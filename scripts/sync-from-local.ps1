param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$TargetCodex = Join-Path $RepoRoot "codex"
$SourceGuidance = Join-Path $CodexHome "AGENTS.md"

if (-not (Test-Path -LiteralPath $SourceGuidance -PathType Leaf)) {
  throw "Missing required file: $SourceGuidance"
}

Copy-Item $SourceGuidance (Join-Path $TargetCodex "AGENTS.md") -Force

Write-Host "Synced local AGENTS.md into $TargetCodex"
Write-Host "Review git diff before committing. config.toml was not read or changed."
