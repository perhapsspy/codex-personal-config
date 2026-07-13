param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SourceCodex = Join-Path $RepoRoot "codex"
$SourceAgents = Join-Path $SourceCodex "agents"
$TargetAgents = Join-Path $CodexHome "agents"
$StatePath = Join-Path $CodexHome ".portable-config-agent-files"
$AgentFiles = @(Get-ChildItem -LiteralPath $SourceAgents -Filter "*.toml" -File)

if (-not (Test-Path -LiteralPath (Join-Path $SourceCodex "AGENTS.md") -PathType Leaf)) {
  throw "Missing required file: $(Join-Path $SourceCodex "AGENTS.md")"
}

if ($AgentFiles.Count -eq 0) {
  throw "No agent TOML files found in $SourceAgents"
}

foreach ($AgentFile in $AgentFiles) {
  $Content = Get-Content -LiteralPath $AgentFile.FullName -Raw
  foreach ($Key in @("name", "description", "developer_instructions")) {
    if (-not [regex]::IsMatch($Content, "(?m)^$Key\s*=")) {
      throw "Missing $Key in $($AgentFile.FullName)"
    }
  }
}

New-Item -ItemType Directory -Force $CodexHome | Out-Null
New-Item -ItemType Directory -Force $TargetAgents | Out-Null

$SourceNames = @($AgentFiles.Name)
Copy-Item (Join-Path $SourceCodex "AGENTS.md") (Join-Path $CodexHome "AGENTS.md") -Force
Copy-Item $AgentFiles.FullName $TargetAgents -Force

if (Test-Path -LiteralPath $StatePath -PathType Leaf) {
  foreach ($PreviousName in Get-Content -LiteralPath $StatePath) {
    if ([string]::IsNullOrWhiteSpace($PreviousName) -or $PreviousName -match '[\\/]') {
      continue
    }

    if ($SourceNames -notcontains $PreviousName) {
      $PreviousPath = Join-Path $TargetAgents $PreviousName
      if (Test-Path -LiteralPath $PreviousPath -PathType Leaf) {
        Remove-Item -LiteralPath $PreviousPath -Force
      }
    }
  }
}

$SourceNames | Sort-Object | Set-Content -LiteralPath $StatePath -Encoding utf8

Write-Host "Installed Codex AGENTS.md and $($AgentFiles.Count) custom agents into $CodexHome"
Write-Host "Removed only stale agent files previously installed by this script."
Write-Host "config.toml was not changed."
