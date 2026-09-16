#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_codex="$repo_root/codex"
source_agents="$source_codex/agents"
codex_home="${CODEX_HOME:-$HOME/.codex}"
target_agents="$codex_home/agents"
state_path="$codex_home/.portable-config-agent-files"
agent_names=("explorer.toml" "worker.toml")

[[ -f "$source_codex/AGENTS.md" ]] || {
  echo "Missing required file: $source_codex/AGENTS.md" >&2
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

mkdir -p "$target_agents"
cp "$source_codex/AGENTS.md" "$codex_home/AGENTS.md"
for agent_name in "${agent_names[@]}"; do
  cp "$source_agents/$agent_name" "$target_agents/$agent_name"
done

if [[ -f "$state_path" ]]; then
  while IFS= read -r previous_name; do
    case "$previous_name" in
      ""|*/*|*\\*) continue ;;
    esac

    keep_previous=false
    for agent_name in "${agent_names[@]}"; do
      [[ "$previous_name" == "$agent_name" ]] && keep_previous=true
    done

    if [[ "$keep_previous" == false && -f "$target_agents/$previous_name" ]]; then
      rm -f "$target_agents/$previous_name"
    fi
  done < "$state_path"
fi

state_temp="$(mktemp "${state_path}.XXXXXX")"
printf '%s\n' "${agent_names[@]}" > "$state_temp"
mv -f "$state_temp" "$state_path"

echo "Installed Codex AGENTS.md and ${#agent_names[@]} custom agents into $codex_home"
echo "Removed only stale agent files previously installed by this script."
echo "config.toml was not changed."
