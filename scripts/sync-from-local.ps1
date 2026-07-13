param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$TargetCodex = Join-Path $RepoRoot "codex"
$TargetAgents = Join-Path $TargetCodex "agents"
$SourceAgents = Join-Path $CodexHome "agents"
$SourceAgentsFile = Join-Path $CodexHome "AGENTS.md"
$AgentFiles = @(Get-ChildItem -LiteralPath $SourceAgents -Filter "*.toml" -File)

if (-not (Test-Path -LiteralPath $SourceAgentsFile -PathType Leaf)) {
  throw "Missing required file: $SourceAgentsFile"
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

Get-ChildItem -LiteralPath $TargetAgents -Filter "*.toml" -File | Remove-Item -Force
Copy-Item $SourceAgentsFile (Join-Path $TargetCodex "AGENTS.md") -Force
Copy-Item $AgentFiles.FullName $TargetAgents -Force

Write-Host "Synced $($AgentFiles.Count) local custom agents and AGENTS.md into $TargetCodex"
Write-Host "Review git diff before committing. config.toml was not read or changed."
