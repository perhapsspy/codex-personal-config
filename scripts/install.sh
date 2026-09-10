#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_codex="$repo_root/codex"
codex_home="${CODEX_HOME:-$HOME/.codex}"
target_agents="$codex_home/agents"
state_path="$codex_home/.portable-config-agent-files"

[[ -f "$source_codex/AGENTS.md" ]] || {
  echo "Missing required file: $source_codex/AGENTS.md" >&2
  exit 1
}

mkdir -p "$codex_home"
cp "$source_codex/AGENTS.md" "$codex_home/AGENTS.md"

removed_count=0
if [[ -f "$state_path" ]]; then
  while IFS= read -r previous_name; do
    case "$previous_name" in
      ""|*/*|*\\*) continue ;;
    esac

    if [[ -f "$target_agents/$previous_name" ]]; then
      rm -f "$target_agents/$previous_name"
      removed_count=$((removed_count + 1))
    fi
  done < "$state_path"
  rm -f "$state_path"
fi

echo "Installed Codex AGENTS.md into $codex_home"
echo "Removed $removed_count custom agent file(s) previously installed by this script."
echo "config.toml was not changed."
