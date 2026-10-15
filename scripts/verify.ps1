param(
  [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" })
)
$ErrorActionPreference = "Stop"
& py -3 (Join-Path $PSScriptRoot "portable_config.py") verify --codex-home $CodexHome
exit $LASTEXITCODE
