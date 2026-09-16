#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_codex="$repo_root/codex"
target_agents="$target_codex/agents"
codex_home="${CODEX_HOME:-$HOME/.codex}"
source_guidance="$codex_home/AGENTS.md"
source_agents="$codex_home/agents"
agent_names=("explorer.toml" "worker.toml")

[[ -f "$source_guidance" ]] || {
  echo "Missing required file: $source_guidance" >&2
  exit 1
}

for agent_name in "${agent_names[@]}"; do
  agent_file="$source_agents/$agent_name"
  [[ -f "$agent_file" ]] || {
    echo "Missing required file: $agent_file" >&2
    exit 1
  }

  for key in name description model model_reasoning_effort sandbox_mode developer_instructions; do
    grep -Eq "^${key}[[:space:]]*=" "$agent_file" || {
      echo "Missing $key in $agent_file" >&2
      exit 1
    }
  done
done

cp "$source_guidance" "$target_codex/AGENTS.md"
for agent_name in "${agent_names[@]}"; do
  cp "$source_agents/$agent_name" "$target_agents/$agent_name"
done

echo "Synced local AGENTS.md and ${#agent_names[@]} managed custom agents into $target_codex"
echo "Review git diff before committing. config.toml was not read or changed."
