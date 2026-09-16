param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceCodex = Join-Path $RepoRoot "codex"
$SourceAgents = Join-Path $SourceCodex "agents"
$TargetAgents = Join-Path $CodexHome "agents"
$StatePath = Join-Path $CodexHome ".portable-config-agent-files"
$AgentNames = @("explorer.toml", "worker.toml")

if (-not (Test-Path -LiteralPath (Join-Path $SourceCodex "AGENTS.md") -PathType Leaf)) {
  throw "Missing required file: $(Join-Path $SourceCodex "AGENTS.md")"
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

New-Item -ItemType Directory -Force $TargetAgents | Out-Null
Copy-Item (Join-Path $SourceCodex "AGENTS.md") (Join-Path $CodexHome "AGENTS.md") -Force
foreach ($AgentName in $AgentNames) {
  Copy-Item (Join-Path $SourceAgents $AgentName) (Join-Path $TargetAgents $AgentName) -Force
}

if (Test-Path -LiteralPath $StatePath -PathType Leaf) {
  foreach ($PreviousName in Get-Content -LiteralPath $StatePath) {
    if ([string]::IsNullOrWhiteSpace($PreviousName) -or $PreviousName -match '[\\/]') {
      continue
    }

    $PreviousPath = Join-Path $TargetAgents $PreviousName
    if ($AgentNames -notcontains $PreviousName -and (Test-Path -LiteralPath $PreviousPath -PathType Leaf)) {
      Remove-Item -LiteralPath $PreviousPath -Force
    }
  }
}

[System.IO.File]::WriteAllLines(
  $StatePath,
  $AgentNames,
  [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Installed Codex AGENTS.md and $($AgentNames.Count) custom agents into $CodexHome"
Write-Host "Removed only stale agent files previously installed by this script."
Write-Host "config.toml was not changed."
