$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Required = @(
  "codex/AGENTS.md",
  "codex/agents/code-mapper.toml",
  "codex/agents/deep-reasoner.toml",
  "codex/agents/docs-researcher.toml",
  "codex/agents/reviewer.toml",
  "codex/agents/routine_worker.toml",
  "scripts/install.ps1",
  "scripts/install.sh"
)

foreach ($Path in $Required) {
  $FullPath = Join-Path $RepoRoot $Path
  if (-not (Test-Path $FullPath)) {
    throw "Missing required file: $Path"
  }
}

foreach ($File in Get-ChildItem (Join-Path $RepoRoot "codex/agents") -Filter "*.toml") {
  $Text = Get-Content $File.FullName -Raw
  foreach ($Field in @("name", "description", "developer_instructions")) {
    if ($Text -notmatch "(?m)^$Field\s*=") {
      throw "$($File.Name) is missing required field: $Field"
    }
  }
}

$Forbidden = @("auth.json", "sessions", "plugins/cache", ".tmp")
foreach ($Item in $Forbidden) {
  if (Test-Path (Join-Path $RepoRoot $Item)) {
    throw "Forbidden runtime state in repo: $Item"
  }
}

Write-Host "Validation passed."
