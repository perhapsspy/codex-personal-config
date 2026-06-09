#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"

mkdir -p "$codex_home/agents"
cp "$repo_root/codex/AGENTS.md" "$codex_home/AGENTS.md"
cp "$repo_root"/codex/agents/*.toml "$codex_home/agents/"

echo "Installed Codex AGENTS.md and custom agents into $codex_home"
echo "config.toml was not changed. Review config/macos.toml.example or config/windows.toml.example as needed."
