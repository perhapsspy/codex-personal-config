#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_codex="$repo_root/codex"
codex_home="${CODEX_HOME:-$HOME/.codex}"
source_guidance="$codex_home/AGENTS.md"

[[ -f "$source_guidance" ]] || {
  echo "Missing required file: $source_guidance" >&2
  exit 1
}

cp "$source_guidance" "$target_codex/AGENTS.md"

echo "Synced local AGENTS.md into $target_codex"
echo "Review git diff before committing. config.toml was not read or changed."
