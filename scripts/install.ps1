param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceCodex = Join-Path $RepoRoot "codex"
$TargetAgents = Join-Path $CodexHome "agents"
$StatePath = Join-Path $CodexHome ".portable-config-agent-files"

if (-not (Test-Path -LiteralPath (Join-Path $SourceCodex "AGENTS.md") -PathType Leaf)) {
  throw "Missing required file: $(Join-Path $SourceCodex "AGENTS.md")"
}

New-Item -ItemType Directory -Force $CodexHome | Out-Null
Copy-Item (Join-Path $SourceCodex "AGENTS.md") (Join-Path $CodexHome "AGENTS.md") -Force

$RemovedCount = 0
if (Test-Path -LiteralPath $StatePath -PathType Leaf) {
  foreach ($PreviousName in Get-Content -LiteralPath $StatePath) {
    if ([string]::IsNullOrWhiteSpace($PreviousName) -or $PreviousName -match '[\\/]') {
      continue
    }

    $PreviousPath = Join-Path $TargetAgents $PreviousName
    if (Test-Path -LiteralPath $PreviousPath -PathType Leaf) {
      Remove-Item -LiteralPath $PreviousPath -Force
      $RemovedCount += 1
    }
  }
  Remove-Item -LiteralPath $StatePath -Force
}

Write-Host "Installed Codex AGENTS.md into $CodexHome"
Write-Host "Removed $RemovedCount custom agent file(s) previously installed by this script."
Write-Host "config.toml was not changed."
