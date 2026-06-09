param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceCodex = Join-Path $RepoRoot "codex"
$SourceAgents = Join-Path $SourceCodex "agents"
$TargetAgents = Join-Path $CodexHome "agents"

foreach ($Path in @(
  (Join-Path $SourceCodex "AGENTS.md"),
  (Join-Path $SourceAgents "code-mapper.toml"),
  (Join-Path $SourceAgents "deep-reasoner.toml"),
  (Join-Path $SourceAgents "docs-researcher.toml"),
  (Join-Path $SourceAgents "reviewer.toml"),
  (Join-Path $SourceAgents "routine_worker.toml")
)) {
  if (-not (Test-Path $Path)) {
    throw "Missing required file: $Path"
  }
}

New-Item -ItemType Directory -Force $CodexHome | Out-Null
New-Item -ItemType Directory -Force $TargetAgents | Out-Null

Copy-Item (Join-Path $SourceCodex "AGENTS.md") (Join-Path $CodexHome "AGENTS.md") -Force
Copy-Item (Join-Path $SourceAgents "*.toml") $TargetAgents -Force

Write-Host "Installed Codex AGENTS.md and custom agents into $CodexHome"
Write-Host "config.toml was not changed."
