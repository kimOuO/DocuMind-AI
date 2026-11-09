#!/usr/bin/env python3
"""Pre-flight and evidence checks for the checkpoint skill. Read-only.

Usage:
    python3 .claude/skills/checkpoint/scripts/check_checkpoint.py \
        --mode session|phase [--tag cp-N-name]

Findings are printed in three groups:
  BLOCKING      the checkpoint must stop (exit code 1)
  NON-BLOCKING  record as pending; the checkpoint may continue
  INFO          context for the final report

Standard library only, so it runs without the project virtualenv.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DECISION_LOG = REPO_ROOT / "docs/05-ai-collaboration/decision-log.md"
RAW_TRANSCRIPTS = REPO_ROOT / "docs/05-ai-collaboration/sessions/raw"
REQUIRED_PATHS = [
    "docs/02-specs",
    "docs/04-dev-journal/TEMPLATE.md",
    "docs/05-ai-collaboration/decision-log.md",
    "docs/05-ai-collaboration/insights.md",
    "Makefile",
]
REQUIRED_MAKE_TARGETS = ["check", "transcript"]
TAG_PATTERN = re.compile(r"^(cp-\d+-[a-z0-9]+(?:-[a-z0-9]+)*|v\d+\.\d+\.\d+)$")
REQUIRED_DECISION_FIELDS = ["我的原始回覆"]

# Secrets block a checkpoint; personal data in tracked files does too.
SENSITIVE = {
    "API key or token": re.compile(
        r"\b(?:sk|pk|ghp|gho|github_pat|xox[abp])[-_][A-Za-z0-9_-]{16,}|\bAKIA[0-9A-Z]{16}\b"
    ),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    # Must end in an alphabetic TLD, so "user@127.0.0.1" in a connection URL is not an email.
    "email address": re.compile(
        r"[\w.+-]+@(?!users\.noreply\.github\.com|anthropic\.com)[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b"
    ),
    "phone number": re.compile(r"\b09\d{2}[- ]?\d{3}[- ]?\d{3}\b"),
}
# Folders of third-party text: the papers, and the evaluation records that quote their pages
# (source snippets carry the authors' published e-mail addresses). Keys are still looked for.
EMAIL_SCAN_EXCLUDE = ("evaluation/", "sample-documents/")
# Files whose job is to describe these patterns, or that hold third-party text.
SENSITIVE_SCAN_EXCLUDE = (
    "package-lock.json",
    "scripts/export_transcript.py",
    ".claude/skills/checkpoint/scripts/check_checkpoint.py",
)


class Report:
    def __init__(self) -> None:
        self.blocking: list[str] = []
        self.pending: list[str] = []
        self.info: list[str] = []

    def print(self) -> int:
        for title, items in (
            ("BLOCKING", self.blocking),
            ("NON-BLOCKING", self.pending),
            ("INFO", self.info),
        ):
            print(f"\n{title} ({len(items)})")
            for item in items:
                print(f"  - {item}")
        print()
        if self.blocking:
            print("Result: BLOCKED. Stop the checkpoint and report to the user.")
            return 1
        print(
            "Result: OK to continue."
            + (" Pending items remain." if self.pending else "")
        )
        return 0


def git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip()


def check_git(report: Report, mode: str, tag: str | None) -> None:
    code, _ = git("rev-parse", "--is-inside-work-tree")
    if code != 0:
        report.blocking.append("Not inside a Git repository.")
        return
    _, branch = git("rev-parse", "--abbrev-ref", "HEAD")
    _, head = git("rev-parse", "--short", "HEAD")
    report.info.append(f"branch={branch} HEAD={head}")
    if branch == "HEAD":
        report.blocking.append("Detached HEAD: check out a branch before a checkpoint.")

    _, status = git("status", "--porcelain")
    changed = [line for line in status.splitlines() if line]
    report.info.append(f"working tree: {len(changed)} changed file(s)")

    _, upstream = git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if upstream:
        behind, ahead = upstream.split()
        report.info.append(f"remote: {ahead} commit(s) ahead, {behind} behind upstream")
        if behind != "0":
            report.blocking.append(
                "Local branch is behind its upstream; sync before tagging."
            )
    else:
        report.info.append("remote: no upstream configured (local only)")

    if mode == "phase" and not tag:
        report.blocking.append(
            "Phase checkpoint needs --tag (confirm the name with the user)."
        )
    if tag:
        if not TAG_PATTERN.match(tag):
            report.blocking.append(
                f"Tag '{tag}' does not match cp-<number>-<outcome> or v<major>.<minor>.<patch>."
            )
        _, existing = git("tag", "--list", tag)
        if existing:
            report.blocking.append(
                f"Tag '{tag}' already exists; tags must not be overwritten."
            )
    _, tags = git("tag", "--list")
    report.info.append(
        "existing checkpoint tags: " + (", ".join(tags.split()) or "none")
    )


def check_project_files(report: Report) -> None:
    for rel in REQUIRED_PATHS:
        if not (REPO_ROOT / rel).exists():
            report.blocking.append(f"Missing required path: {rel}")
    makefile = REPO_ROOT / "Makefile"
    if makefile.exists():
        text = makefile.read_text(encoding="utf-8")
        for target in REQUIRED_MAKE_TARGETS:
            if not re.search(rf"^{target}:", text, re.MULTILINE):
                report.blocking.append(f"Makefile has no '{target}' target.")


def check_decision_log(report: Report) -> None:
    if not DECISION_LOG.exists():
        return
    text = DECISION_LOG.read_text(encoding="utf-8")
    sections = re.split(r"^### ", text, flags=re.MULTILINE)[1:]
    ids = [re.match(r"D\d+", s).group(0) for s in sections if re.match(r"D\d+", s)]
    report.info.append(
        f"decision log: {len(set(ids))} decision(s) with a detail section"
    )

    for section in sections:
        title = section.splitlines()[0]
        # Combined or supplementary sections follow their own layout.
        if "／" in title or "補充" in title:
            continue
        for field in REQUIRED_DECISION_FIELDS:
            if field not in section:
                report.pending.append(f"decision log: '{title}' has no '{field}' field")
        if "待回填" in section:
            report.pending.append(
                f"decision log: '{title}' still has a commit to fill in"
            )
        if "待確認" in section:
            report.pending.append(
                f"decision log: '{title}' is waiting for the user's confirmation"
            )

    overview_ids = set(re.findall(r"^\| (D\d+) \|", text, re.MULTILINE))
    detailed = {
        i for section in sections for i in re.findall(r"D\d+", section.splitlines()[0])
    }
    for missing in sorted(overview_ids - detailed):
        report.pending.append(
            f"decision log: {missing} is in the overview but has no detail section"
        )


def check_sensitive(report: Report) -> None:
    _, listing = git("ls-files")
    tracked = [REPO_ROOT / line for line in listing.splitlines() if line]
    untracked_transcripts = (
        list(RAW_TRANSCRIPTS.glob("*.md")) if RAW_TRANSCRIPTS.is_dir() else []
    )
    seen: set[Path] = set()
    # docs/ is kept out of git, so scan it from disk as well.
    local_docs = [
        d for d in (REPO_ROOT / "docs").rglob("*.md") if "archive" not in d.parts
    ]
    for path in [*tracked, *untracked_transcripts, *local_docs]:
        rel = path.relative_to(REPO_ROOT).as_posix()
        if path in seen or rel.endswith(SENSITIVE_SCAN_EXCLUDE) or not path.is_file():
            continue
        seen.add(path)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary file
        for label, pattern in SENSITIVE.items():
            if label == "email address" and rel.startswith(EMAIL_SCAN_EXCLUDE):
                continue
            for match in pattern.finditer(text):
                line_start = text.rfind("\n", 0, match.start()) + 1
                # "git@github.com:owner/repo.git" is an SSH remote, not an email address.
                if (
                    label == "email address"
                    and text[match.end() : match.end() + 1] == ":"
                ):
                    continue
                # "scheme://user:password@host" is a connection URL, not an email address.
                if (
                    label == "email address"
                    and "://" in text[line_start : match.start()]
                ):
                    continue
                line = text.count("\n", 0, match.start()) + 1
                report.blocking.append(f"possible {label} in {rel}:{line}")
                break
    report.info.append(f"sensitive-data scan: {len(seen)} text file(s) checked")
    if not untracked_transcripts:
        report.pending.append("no exported transcript found; run `make transcript`")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Checkpoint pre-flight checks (read-only)."
    )
    parser.add_argument("--mode", choices=["session", "phase"], required=True)
    parser.add_argument(
        "--tag", help="tag to create, e.g. cp-2-mvp (required for phase mode)"
    )
    args = parser.parse_args()

    report = Report()
    report.info.append(f"mode={args.mode} tag={args.tag or '-'}")
    check_git(report, args.mode, args.tag)
    check_project_files(report)
    check_decision_log(report)
    check_sensitive(report)
    return report.print()


if __name__ == "__main__":
    sys.exit(main())
