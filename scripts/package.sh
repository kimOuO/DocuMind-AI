#!/usr/bin/env bash
# Build the delivery zip from the committed tree (HEAD), so nothing untracked,
# ignored or secret can leak into the package.
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree has uncommitted changes; commit or stash them first." >&2
  exit 1
fi

version="$(git describe --tags --always)"
out="DocuMind-AI-${version}.zip"

git archive --format=zip --prefix=DocuMind-AI/ -o "${out}" HEAD
echo "Created ${out} ($(du -h "${out}" | cut -f1))"
