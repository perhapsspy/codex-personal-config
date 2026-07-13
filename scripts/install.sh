#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_codex="$repo_root/codex"
source_agents="$source_codex/agents"
codex_home="${CODEX_HOME:-$HOME/.codex}"
target_agents="$codex_home/agents"
state_path="$codex_home/.portable-config-agent-files"

[[ -f "$source_codex/AGENTS.md" ]] || {
  echo "Missing required file: $source_codex/AGENTS.md" >&2
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

mkdir -p "$target_agents"
cp "$source_codex/AGENTS.md" "$codex_home/AGENTS.md"
cp "${agent_files[@]}" "$target_agents/"

if [[ -f "$state_path" ]]; then
  while IFS= read -r previous_name; do
    case "$previous_name" in
      ""|*/*|*\\*) continue ;;
    esac

    if [[ ! -f "$source_agents/$previous_name" && -f "$target_agents/$previous_name" ]]; then
      rm -f "$target_agents/$previous_name"
    fi
  done < "$state_path"
fi

state_temp="$(mktemp "${state_path}.XXXXXX")"
for agent_file in "${agent_files[@]}"; do
  basename "$agent_file"
done | sort > "$state_temp"
mv -f "$state_temp" "$state_path"

echo "Installed Codex AGENTS.md and ${#agent_files[@]} custom agents into $codex_home"
echo "Removed only stale agent files previously installed by this script."
echo "config.toml was not changed."
