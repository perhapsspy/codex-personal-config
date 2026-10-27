# Codex Personal Config

Portable personal Codex guidance, support-agent definitions, and core model defaults for `perhapsspy`.

The installable source lives in [codex/](codex/). Installation applies the managed guidance, agent definitions, and shared defaults to the selected Codex home.

Auth, sessions, caches, memories, plugin state, app-generated paths, and project trust lists stay local. Only declared shared settings are managed in `config.toml`.

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

The installer copies managed guidance and agent definitions, merges declared shared settings into local `config.toml`, and removes only stale agents it previously installed. Other local settings and personal agents are preserved. It then reads the installed files and declared settings back to verify they match the source.

After installation, confirm the effective model, reasoning effort, and Standard speed in the client. Speed settings remain local and are not changed by this installer.

To install into a non-default Codex home, set `CODEX_HOME` on macOS/Linux or pass `-CodexHome` in PowerShell.

```bash
CODEX_HOME="$HOME/.codex-test" ./scripts/install.sh
```

```powershell
.\scripts\install.ps1 -CodexHome "$HOME\.codex-test"
```

## Deployment targets

Use this repository as the shared source for the Mac, the Codex running on the dot's cloud instance, and Windows. Installation runs on each target; publishing this repository does not update the other machines.

| Target | How it is updated | Evidence required |
| --- | --- | --- |
| Mac | Run the installer in the local checkout. | Source revision, host, actual Codex home, and verification result. |
| Dot instance | Run the same installer through a supported execution path on the dot's own cloud computer. | Its own host and Codex home, source revision, supported Codex installation, and verification result. |
| Windows | Pull the repository and run the PowerShell installer manually. | The Windows verification output; otherwise report that its manual update is pending. |

For each deployment or sync, report the targets separately as verified, pending, or blocked. If a target is unavailable, finish the accessible targets and name the missing connection or manual step. A successful Mac run, a cloud task label, or a message sent to the dot is not evidence of installation on the dot instance.

Before installing, identify the Codex process's actual `CODEX_HOME` and the host's supported Codex version. An existing profile or session override may change effective settings. Verification checks saved files and declared defaults; it does not prove a running session has reloaded them or that the host supports every configured role. Check those separately in the target client when claiming runtime activation.

Use the existing checkout when available. Preserve local changes and inspect the remote and current branch before updating. On macOS/Linux:

```bash
git pull --ff-only && ./scripts/install.sh
```

On Windows, stop if the update fails before starting installation:

```powershell
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Repository update failed; installation stopped." }
.\scripts\install.ps1
```

Compare `git rev-parse HEAD` with the revision being deployed. If a checkout has local changes or a different revision, reconcile it without discarding work before claiming that revision is installed. Install the Python dependency described above on a new machine.

To check an installation without changing it:

```bash
./scripts/verify.sh
```

```powershell
.\scripts\verify.ps1
```

Both verification wrappers accept the same Codex-home override as their installer (`--codex-home` or `-CodexHome`). Verification reports host, platform, source location/revision, Codex home, and check time. A missing or mismatched managed file or declared setting returns a nonzero exit status. Unmanaged settings are outside that comparison.

### Applying to the dot instance

The dot's cloud computer and the connected Mac are separate execution targets. Use an available supported remote connection or explicitly ask the dot to execute the deployment on its own cloud computer. Verify the destination before writing; do not substitute the connected Mac when the cloud destination is unavailable. The product distinction is described in [Meet dots](https://learn.chatgpt.com/docs/dots).

When handing off to the dot, give it the published revision and this bounded request:

```text
Install perhapsspy/codex-personal-config at revision <published commit> on the Codex running on your own cloud instance.
First report the actual host/OS, Codex executable/version, and effective CODEX_HOME; distinguish this environment from the connected Mac.
Use existing authorized repository access and preserve local changes. Obtain the requested revision without force-updating an existing checkout.
Run the repository's scripts/install.sh against that Codex home, then scripts/verify.sh. Preserve credentials, permissions, MCP settings, session data, and other unmanaged settings.
Return the source revision and verification output, plus any role-support or running-session reload limitation. Do not print credentials or the full local config.
If your cloud instance cannot run Codex or does not expose a supported installation path, report that target as blocked instead of applying to another host.
```

If the cloud Codex home is ephemeral, repeat the same installation when that environment is recreated. Determine persistence on the target; do not assume an installation survives recreation.

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

The sync command imports managed guidance, agent definitions, and allowed shared settings from the selected Codex home. Other local settings and agents are ignored. Missing input files or invalid TOML stop the command before updates.

Sync is an explicit import from the selected host into the repository. Run it only when that host's shared settings are the intended new source. To receive published changes on another machine, use install, not sync.

## Shared configuration flow

1. Adjust the shared guidance, managed agents, or core settings on one machine.
2. Run the sync command above when the source change began in the local Codex home.
3. Run the repository validation:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

4. Review `git diff`.
5. Commit and push this repository.
6. Apply that revision to the Mac and the dot instance using the target workflow above; report each result independently.
7. Provide the revision and PowerShell command for the manual Windows update, and keep its status pending until Windows verification is available.

Validation checks the portable agent contracts and install/sync behavior.

## Editing shared configuration

Edit startup behavior in [the shared guidance](codex/AGENTS.md), agent definitions in [codex/agents/](codex/agents/), and shared defaults in [codex/config.shared.toml](codex/config.shared.toml).

Each agent definition owns its selection description, model, effort, and execution instructions.

Custom agents inherit the parent session's permissions. Read-only role instructions constrain behavior but do not establish a separate read-only sandbox. Use the current runtime tools to confirm available role selection and effective permissions. See the [official custom-agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agent-file-schema).

Installation applies only keys present in the shared file; omitting a key leaves its local value unchanged. Sync exports only managed keys present locally. Approval, sandbox, MCP, plugin, desktop, and project settings remain machine-local.
