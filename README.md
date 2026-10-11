# Codex Personal Config

Portable personal Codex guidance, support-agent definitions, and core model defaults for `perhapsspy`.

This repository is the shared source for files that should follow you between machines:

- `codex/AGENTS.md` -> `~/.codex/AGENTS.md`
- `codex/agents/worker.toml` -> `~/.codex/agents/worker.toml`
- `codex/agents/explorer.toml` -> `~/.codex/agents/explorer.toml`
- `codex/agents/advisor.toml` -> `~/.codex/agents/advisor.toml`
- `codex/config.shared.toml` -> selected keys in `~/.codex/config.toml`

Auth, sessions, caches, memories, plugin state, app-generated paths, and project trust lists stay local. Only the core keys listed below are shared from `config.toml`.

## Apply the repository on a machine

The scripts require Python 3.11+ and `tomlkit`, which preserves local TOML formatting and comments. Install the dependency once from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

On Windows, use `py -3 -m pip install -r requirements.txt`.

With `uv`, skip the separate dependency install and prefix either script command with `uv run --with-requirements requirements.txt`.

Run the installer after pulling changes.

macOS or Linux:

```bash
./scripts/install.sh
```

Windows PowerShell:

```powershell
.\scripts\install.ps1
```

If PowerShell blocks local scripts, run this once in that shell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

The installer copies `AGENTS.md` and the three managed agent TOMLs, merges declared core settings into local `config.toml`, and removes only stale agents it previously installed. Other local settings and personal agents are preserved.

After installation, confirm the effective model, reasoning effort, and Standard speed in the client. Speed settings remain local and are not changed by this installer.

To install into a non-default Codex home, set `CODEX_HOME` on macOS/Linux or pass `-CodexHome` in PowerShell.

```bash
CODEX_HOME="$HOME/.codex-test" ./scripts/install.sh
```

```powershell
.\scripts\install.ps1 -CodexHome "$HOME\.codex-test"
```

## Promote local shared settings into this repository

When you intentionally update the shared settings on a machine, run the sync command from this repository.

macOS or Linux:

```bash
./scripts/sync-from-local.sh
```

Windows PowerShell:

```powershell
.\scripts\sync-from-local.ps1
```

The sync command copies local `AGENTS.md`, `worker.toml`, `explorer.toml`, and `advisor.toml` into the repository and extracts only the five core keys into `codex/config.shared.toml`. Other local settings and agents are ignored. Missing input files or invalid TOML stop the command before updates.

## Shared configuration flow

1. Adjust the shared guidance, managed agents, or core settings on one machine.
2. Run the sync command above when the source change began in the local Codex home.
3. Run the repository validation:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

4. Review `git diff`.
5. Commit and push this repository.
6. On another machine, pull and run the installer.

Validation checks the portable agent contracts and install/sync behavior.

## Delegation roles

The main session and default subagents use GPT-6.1 Sol High; Sol reasoning effort is capped at High.

- `worker` uses GPT-6.1 Sol High for bounded implementation, fixes, refactoring, and tests.
- `explorer` uses Luna Max for code or documentation investigation, log analysis, and checks against explicit criteria.
- `advisor` uses GPT-6 Astra High with a read-only sandbox default for independent direction, structure, and strong review, including dots and Sol assumptions and completion claims. It compares original requests and approved scope with plans, code, changes, and validation evidence. The main session owns final acceptance.

Consult advisor at substantial work kickoff, after important user-facing feature groups, before declaring no remaining work, and immediately when Sol suspects direction, structure, omissions, or repetition. Avoid repeated consultation on unchanged evidence or every simple task or commit. Worker may delegate only advisor consultation; if nested calls are unavailable, the main session must relay the request without changing call limits. Continue independent work and hold only affected decisions and unreviewed completion claims.

Independent work can reuse a role. Delegation scope, context inheritance, ownership, and completion follow [the shared guidance](codex/AGENTS.md#위임). The standalone role files follow the [official custom-agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agent-file-schema). Runtime tools and live parent permission overrides determine available calls and effective permissions; verify them in the current session.

## Core configuration

Edit [codex/config.shared.toml](codex/config.shared.toml) to change the shared defaults. The managed keys are:

- `model`
- `model_reasoning_effort`
- `agents.max_concurrent_threads_per_session`
- `agents.default_subagent_model`
- `agents.default_subagent_reasoning_effort`

Installation applies only keys present in the shared file; omitting a key leaves its local value unchanged. Sync exports only managed keys present locally. Approval, sandbox, MCP, plugin, desktop, and project settings remain machine-local.

The role TOMLs set model and effort for `worker`, `explorer`, and `advisor`; the shared `[agents]` defaults apply to children without a role-specific override.
