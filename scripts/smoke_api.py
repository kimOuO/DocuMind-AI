#!/usr/bin/env python3
"""API test of the running deployment, run after a backend or frontend change is deployed.

    health -> register and log in -> upload the sample paper -> wait until it is ready
    -> a question (sources, citations, usage) -> a follow-up (judged, rewritten)
    -> a question the document does not cover -> the ledger (every call within the limit)

It talks to the deployment only through its public API, as the browser does, and removes
the conversation and the document it created. Run with `make smoke-api` after `make up`
(or `python scripts/smoke_api.py http://host:port`). Exits 0 when every check passes.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import httpx

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3000").rstrip("/")
API = f"{BASE}/api/v1"
PAPER = Path(__file__).resolve().parents[1] / "sample-documents" / "2410.05779v3.pdf"
PASSWORD = "smoke-api-2026"
failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(
        f"{'PASS' if ok else 'FAIL'}  {name}{'  — ' + detail if detail else ''}",
        flush=True,
    )
    if not ok:
        failures.append(name)


def ask(client: httpx.Client, conversation: str, question: str, document: str) -> dict:
    """Ask one question and collect the events of its answer stream."""
    events: list[tuple[str, dict]] = []
    body = {"question": question, "document_ids": [document], "temperature": 0}
    with client.stream(
        "POST", f"{API}/conversations/{conversation}/messages", json=body
    ) as r:
        r.raise_for_status()
        name = None
        for line in r.iter_lines():
            if line.startswith("event: "):
                name = line[7:]
            elif line.startswith("data: ") and name:
                events.append((name, json.loads(line[6:])))
    found = dict(events)
    found["answer"] = "".join(data["text"] for name, data in events if name == "delta")
    return found


def main() -> int:
    client = httpx.Client(headers={"Origin": BASE}, timeout=900)
    health = client.get(f"{API}/health").json()
    check("health is ok", health.get("status") == "ok", json.dumps(health)[:120])
    limit = health.get("llm_context_limit", 10_000)

    user = f"smoke{int(time.time()) % 1_000_000}"
    client.post(f"{API}/auth/register", json={"username": user, "password": PASSWORD})
    check(
        "register and log in",
        client.post(
            f"{API}/auth/login", json={"username": user, "password": PASSWORD}
        ).status_code
        == 200,
    )

    with PAPER.open("rb") as file:
        upload = client.post(
            f"{API}/documents",
            files={"file": (PAPER.name, file, "application/pdf")},
            data={"build_summary": "false"},
        )
    check(
        "upload accepted",
        upload.status_code in (200, 201, 202),
        str(upload.status_code),
    )
    document = upload.json()["id"]
    state: dict = {}
    for _ in range(100):
        state = client.get(f"{API}/documents/{document}").json()
        if state["status"] in ("ready", "failed"):
            break
        time.sleep(3)
    check(
        "document indexed",
        state.get("status") == "ready",
        f"{state.get('chunk_count')} chunks",
    )

    conversation = client.post(f"{API}/conversations", json={"title": "smoke"}).json()[
        "id"
    ]
    first = ask(
        client, conversation, "What datasets does the paper evaluate on?", document
    )
    usage = first.get("usage") or {}
    check(
        "answer names the datasets",
        "Agriculture" in first["answer"] and "Legal" in first["answer"],
    )
    check(
        "answer cites its sources",
        bool((first.get("done") or {}).get("cited")) and bool(first.get("sources")),
    )
    check(
        "answer call within the limit",
        0
        < (usage.get("prompt_tokens") or 0) + (usage.get("completion_tokens") or 0)
        <= limit,
        str(usage.get("breakdown")),
    )

    second = ask(client, conversation, "每個有幾份文件？", document)
    route = second.get("route") or {}
    purposes = [
        call["purpose"] for call in (second.get("usage") or {}).get("breakdown", [])
    ]
    check(
        "follow-up is judged and rewritten",
        route.get("follow_up") is True and "rewrite" in purposes,
        f"{route.get('standalone_question')!r} {purposes}",
    )
    check(
        "follow-up answer has the figures",
        "94" in second["answer"] and "12" in second["answer"],
    )

    third = ask(client, conversation, "如何在家烤酸種麵包？", document)
    check(
        "an uncovered question is not answered from the document",
        (third.get("done") or {}).get("answered") is False,
        third["answer"][:60],
    )

    stored = client.get(f"{API}/conversations/{conversation}").json()["messages"]
    check(
        "every stored answer keeps its usage",
        all(m.get("usage") for m in stored if m["role"] == "assistant"),
    )

    ledger = client.get(f"{API}/llm-calls").json()
    measured = ledger.get("measured", {})
    check(
        "every call in the ledger is within the limit",
        (measured.get("max_total_tokens") or 0) <= limit
        and ledger.get("underestimate_events") == 0,
        f"max {measured.get('max_total_tokens')} of {limit}",
    )

    client.delete(f"{API}/conversations/{conversation}")
    client.delete(f"{API}/documents/{document}")
    print(
        f"\n{'ALL CHECKS PASSED' if not failures else 'FAILED: ' + ', '.join(failures)}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
