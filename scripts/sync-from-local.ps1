param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$TargetCodex = Join-Path $RepoRoot "codex"
$TargetAgents = Join-Path $TargetCodex "agents"
$SourceGuidance = Join-Path $CodexHome "AGENTS.md"
$SourceAgents = Join-Path $CodexHome "agents"
$AgentNames = @("explorer.toml", "worker.toml")

if (-not (Test-Path -LiteralPath $SourceGuidance -PathType Leaf)) {
  throw "Missing required file: $SourceGuidance"
}

foreach ($AgentName in $AgentNames) {
  $AgentPath = Join-Path $SourceAgents $AgentName
  if (-not (Test-Path -LiteralPath $AgentPath -PathType Leaf)) {
    throw "Missing required file: $AgentPath"
  }

  $Content = Get-Content -LiteralPath $AgentPath -Raw
  foreach ($Key in @("name", "description", "model", "model_reasoning_effort", "sandbox_mode", "developer_instructions")) {
    if (-not [regex]::IsMatch($Content, "(?m)^$Key\s*=")) {
      throw "Missing $Key in $AgentPath"
    }
  }
}

Copy-Item $SourceGuidance (Join-Path $TargetCodex "AGENTS.md") -Force
foreach ($AgentName in $AgentNames) {
  Copy-Item (Join-Path $SourceAgents $AgentName) (Join-Path $TargetAgents $AgentName) -Force
}

Write-Host "Synced local AGENTS.md and $($AgentNames.Count) managed custom agents into $TargetCodex"
Write-Host "Review git diff before committing. config.toml was not read or changed."
