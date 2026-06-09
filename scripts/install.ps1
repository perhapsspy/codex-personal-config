param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceCodex = Join-Path $RepoRoot "codex"
$SourceAgents = Join-Path $SourceCodex "agents"
$TargetAgents = Join-Path $CodexHome "agents"

New-Item -ItemType Directory -Force $CodexHome | Out-Null
New-Item -ItemType Directory -Force $TargetAgents | Out-Null

Copy-Item (Join-Path $SourceCodex "AGENTS.md") (Join-Path $CodexHome "AGENTS.md") -Force
Copy-Item (Join-Path $SourceAgents "*.toml") $TargetAgents -Force

Write-Host "Installed Codex AGENTS.md and custom agents into $CodexHome"
Write-Host "config.toml was not changed. Review config\\windows.toml.example for Windows-specific defaults."
