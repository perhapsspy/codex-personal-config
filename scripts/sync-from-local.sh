#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_codex="$repo_root/codex"
target_agents="$target_codex/agents"
codex_home="${CODEX_HOME:-$HOME/.codex}"
source_agents="$codex_home/agents"
source_agents_file="$codex_home/AGENTS.md"

[[ -f "$source_agents_file" ]] || {
  echo "Missing required file: $source_agents_file" >&2
  exit 1
}

shopt -s nullglob
agent_files=("$source_agents"/*.toml)
[[ ${#agent_files[@]} -gt 0 ]] || {
  echo "No agent TOML files found in $source_agents" >&2
  exit 1
}

for agent_file in "${agent_files[@]}"; do
  for key in name description developer_instructions; do
    grep -Eq "^${key}[[:space:]]*=" "$agent_file" || {
      echo "Missing $key in $agent_file" >&2
      exit 1
    }
  done
done

rm -f "$target_agents"/*.toml
cp "$source_agents_file" "$target_codex/AGENTS.md"
cp "${agent_files[@]}" "$target_agents/"

echo "Synced ${#agent_files[@]} local custom agents and AGENTS.md into $target_codex"
echo "Review git diff before committing. config.toml was not read or changed."
