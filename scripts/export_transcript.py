#!/usr/bin/env python3
"""Export Claude Code session logs for this project as readable Markdown.

Claude Code stores every session as JSON Lines under
``~/.claude/projects/<project-slug>/<session-id>.jsonl``. This script turns each
session into ``docs/ai-collab/sessions/raw/<date>-<session-id[:8]>.md`` so the
human-AI interaction can be kept as evidence without manual transcription.

What is kept: what the user typed, what the assistant replied, the questions the
assistant asked together with the user's answers, plan approvals/rejections, and
a one-line trace of each tool call. Tool output and model reasoning are left
out: they are bulky and may contain data that should not be shared.

Emails, phone numbers and key-like strings are masked.

Usage: python3 scripts/export_transcript.py [--project-dir DIR] [--out DIR]
Standard library only, so it runs without the project virtualenv.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "docs" / "ai-collab" / "sessions" / "raw"

REDACTIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[email]"),
    (re.compile(r"\b09\d{2}[- ]?\d{3}[- ]?\d{3}\b"), "[phone]"),
    (
        re.compile(r"\b(?:sk|pk|ghp|gho|github_pat|xox[abp])[-_][A-Za-z0-9_-]{16,}"),
        "[secret]",
    ),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[secret]"),
]
SYSTEM_BLOCK = re.compile(
    r"<(system-reminder|local-command-caveat|command-name|command-message|command-args|"
    r"local-command-stdout|task-notification)>.*?</\1>",
    re.DOTALL,
)
# Tool results that carry a decision made by the user.
USER_DECISION_TOOLS = {"AskUserQuestion", "ExitPlanMode"}
TOOL_LABEL_KEYS = ("description", "file_path", "query", "skill", "url")


def default_project_dir() -> Path:
    slug = str(REPO_ROOT).replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug


def redact(text: str) -> str:
    for pattern, replacement in REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


def clean(text: str) -> str:
    return redact(SYSTEM_BLOCK.sub("", text)).strip()


def block_text(content: Any) -> str:
    """Flatten a tool_result ``content`` field (string or list of blocks) to text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def render_question(tool_input: dict[str, Any]) -> str:
    lines = []
    for question in tool_input.get("questions", []):
        lines.append(f"**提問：{question.get('question', '')}**")
        for option in question.get("options", []):
            lines.append(
                f"- {option.get('label', '')}：{option.get('description', '')}"
            )
        lines.append("")
    return "\n".join(lines).strip()


def render_tool_call(name: str, tool_input: dict[str, Any]) -> str:
    label = next((str(tool_input[k]) for k in TOOL_LABEL_KEYS if tool_input.get(k)), "")
    label = label.replace(str(REPO_ROOT) + "/", "")
    return f"- `{name}`" + (f"：{label[:120]}" if label else "")


def render_user_decision(tool_name: str, text: str) -> str:
    if tool_name == "ExitPlanMode":
        # An approval echoes the whole plan back; the plan itself lives in the repo.
        text = text.split("## Approved Plan:")[0]
    return clean(text)


def convert(session_file: Path) -> tuple[str, str] | None:
    """Return (start_date, markdown) for one session, or None if it has no dialogue."""
    sections: list[str] = []
    tool_names: dict[str, str] = {}
    tool_trace: list[str] = []
    timestamps: list[str] = []
    user_turns = 0
    user_decisions = 0

    def flush_tools() -> None:
        if tool_trace:
            sections.append("**Claude 執行的動作**\n\n" + "\n".join(tool_trace))
            tool_trace.clear()

    def add(heading: str, body: str) -> None:
        if body:
            flush_tools()
            sections.append(f"### {heading}\n\n{body}")

    with session_file.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = entry.get("type")
            if kind not in ("user", "assistant") or entry.get("isSidechain"):
                continue
            if entry.get("timestamp"):
                timestamps.append(entry["timestamp"])
            content = entry.get("message", {}).get("content")

            if kind == "user":
                if isinstance(content, str):
                    if not entry.get("isMeta") and clean(content):
                        user_turns += 1
                        add("使用者", clean(content))
                    continue
                for block in content or []:
                    if block.get("type") == "text" and not entry.get("isMeta"):
                        if clean(block.get("text", "")):
                            user_turns += 1
                            add("使用者", clean(block["text"]))
                    elif block.get("type") == "tool_result":
                        tool_name = tool_names.get(block.get("tool_use_id", ""), "")
                        if tool_name in USER_DECISION_TOOLS:
                            user_decisions += 1
                            body = render_user_decision(
                                tool_name, block_text(block.get("content"))
                            )
                            add(f"使用者的回覆（{tool_name}）", body)
            else:
                for block in content or []:
                    if block.get("type") == "text":
                        add("Claude", clean(block.get("text", "")))
                    elif block.get("type") == "tool_use":
                        name = block.get("name", "")
                        tool_names[block.get("id", "")] = name
                        if name == "AskUserQuestion":
                            add(
                                "Claude 提問",
                                redact(render_question(block.get("input", {}))),
                            )
                        elif name == "ExitPlanMode":
                            add("Claude", "（送出計畫，請使用者審核）")
                        else:
                            tool_trace.append(
                                render_tool_call(name, block.get("input", {}))
                            )
    flush_tools()

    if user_turns == 0 or not timestamps:
        return None
    start, end = min(timestamps), max(timestamps)
    header = (
        f"# Claude Code 對話逐字稿 {start[:10]}\n\n"
        f"- Session：`{session_file.stem}`\n"
        f"- 期間（UTC）：{start[:19]} → {end[:19]}\n"
        f"- 使用者輸入訊息：{user_turns} 則；回覆提問與審核計畫：{user_decisions} 次\n"
        "- 由 `scripts/export_transcript.py` 自動產生。工具輸出與模型推理未收錄；"
        "電子郵件、電話、金鑰已遮蔽。\n"
    )
    return start[:10], header + "\n---\n\n" + "\n\n".join(sections) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project-dir", type=Path, default=default_project_dir())
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    if not args.project_dir.is_dir():
        print(f"No Claude Code logs found at {args.project_dir}", file=sys.stderr)
        return 1
    args.out.mkdir(parents=True, exist_ok=True)

    written = 0
    for session_file in sorted(args.project_dir.glob("*.jsonl")):
        result = convert(session_file)
        if result is None:
            continue
        date, markdown = result
        target = args.out / f"{date}-{session_file.stem[:8]}.md"
        target.write_text(markdown, encoding="utf-8")
        written += 1
        print(f"wrote {target.relative_to(REPO_ROOT)}")
    print(f"{written} session(s) exported")
    return 0


if __name__ == "__main__":
    sys.exit(main())
