import os
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_ROOT = REPO_ROOT / "codex"
AGENT_ROOT = CODEX_ROOT / "agents"
AGENT_CONTRACTS = {
    "explorer": ("gpt-5.6-luna", "max", "workspace-write"),
    "worker": ("gpt-5.6-sol", "medium", "workspace-write"),
}
REQUIRED_STRING_FIELDS = (
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
    "developer_instructions",
)


class PortableConfigTests(unittest.TestCase):
    def _copy_portable_repo(self, destination):
        shutil.copytree(CODEX_ROOT, destination / "codex")
        shutil.copytree(REPO_ROOT / "scripts", destination / "scripts")

    def _run_bash_script(self, repo_root, script_name, codex_home, check=True):
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        return subprocess.run(
            ["bash", str(repo_root / "scripts" / script_name)],
            cwd=repo_root,
            env=environment,
            check=check,
            capture_output=True,
            text=True,
        )

    def test_installable_files_and_agent_contracts(self):
        installed_files = sorted(
            path.relative_to(CODEX_ROOT)
            for path in CODEX_ROOT.rglob("*")
            if path.is_file()
        )
        self.assertEqual(
            installed_files,
            [
                Path("AGENTS.md"),
                Path("agents/explorer.toml"),
                Path("agents/worker.toml"),
            ],
        )

        for name, (model, effort, sandbox_mode) in AGENT_CONTRACTS.items():
            with self.subTest(agent=name):
                data = tomllib.loads(
                    (AGENT_ROOT / f"{name}.toml").read_text(encoding="utf-8")
                )
                for field in REQUIRED_STRING_FIELDS:
                    self.assertIsInstance(data.get(field), str)
                    self.assertTrue(data[field].strip())
                self.assertEqual(data["name"], name)
                self.assertEqual(data["model"], model)
                self.assertEqual(data["model_reasoning_effort"], effort)
                self.assertEqual(data["sandbox_mode"], sandbox_mode)

    def test_readme_documents_machine_local_defaults(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn('model = "gpt-6-astra"', readme)
        self.assertIn('model_reasoning_effort = "xhigh"', readme)
        self.assertIn("[agents]", readme)
        self.assertIn('default_subagent_model = "gpt-5.6-sol"', readme)
        self.assertIn('default_subagent_reasoning_effort = "medium"', readme)

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_installer_installs_reinstalls_and_preserves_local_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "repo"
            codex_home = temp_root / ".codex"
            agent_root = codex_home / "agents"
            self._copy_portable_repo(repo_root)
            agent_root.mkdir(parents=True)

            stale_names = [
                "code_mapper.toml",
                "decision_reviewer.toml",
                "docs_researcher.toml",
                "frontend_worker.toml",
                "reviewer.toml",
                "routine_worker.toml",
                "verification_worker.toml",
            ]
            for name in stale_names:
                (agent_root / name).write_text("stale\n", encoding="utf-8")
            (agent_root / "worker.toml").write_text("old worker\n", encoding="utf-8")
            personal_agent = agent_root / "personal.toml"
            personal_agent.write_text("personal\n", encoding="utf-8")
            state_path = codex_home / ".portable-config-agent-files"
            state_path.write_text(
                "\n".join([*stale_names, "worker.toml", "../outside.toml"]) + "\n",
                encoding="utf-8",
            )
            config_path = codex_home / "config.toml"
            config_path.write_text("sentinel = true\n", encoding="utf-8")

            self._run_bash_script(repo_root, "install.sh", codex_home)
            self._run_bash_script(repo_root, "install.sh", codex_home)

            self.assertEqual(
                (codex_home / "AGENTS.md").read_bytes(),
                (repo_root / "codex" / "AGENTS.md").read_bytes(),
            )
            for name in AGENT_CONTRACTS:
                filename = f"{name}.toml"
                self.assertEqual(
                    (agent_root / filename).read_bytes(),
                    (repo_root / "codex" / "agents" / filename).read_bytes(),
                )
            for name in stale_names:
                self.assertFalse((agent_root / name).exists())
            self.assertEqual(personal_agent.read_text(encoding="utf-8"), "personal\n")
            self.assertEqual(
                state_path.read_text(encoding="utf-8").splitlines(),
                ["explorer.toml", "worker.toml"],
            )
            self.assertEqual(config_path.read_text(encoding="utf-8"), "sentinel = true\n")

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_sync_copies_only_managed_agents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "repo"
            codex_home = temp_root / ".codex"
            local_agents = codex_home / "agents"
            self._copy_portable_repo(repo_root)
            local_agents.mkdir(parents=True)

            (codex_home / "AGENTS.md").write_text("local guidance\n", encoding="utf-8")
            for name in AGENT_CONTRACTS:
                filename = f"{name}.toml"
                source = AGENT_ROOT / filename
                (local_agents / filename).write_text(
                    source.read_text(encoding="utf-8") + "\n# local\n",
                    encoding="utf-8",
                )
            (local_agents / "personal.toml").write_text("personal\n", encoding="utf-8")

            self._run_bash_script(repo_root, "sync-from-local.sh", codex_home)

            self.assertEqual(
                (repo_root / "codex" / "AGENTS.md").read_text(encoding="utf-8"),
                "local guidance\n",
            )
            for name in AGENT_CONTRACTS:
                filename = f"{name}.toml"
                self.assertEqual(
                    (repo_root / "codex" / "agents" / filename).read_bytes(),
                    (local_agents / filename).read_bytes(),
                )
            self.assertFalse((repo_root / "codex" / "agents" / "personal.toml").exists())

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_sync_missing_input_does_not_partially_update(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = temp_root / "repo"
            codex_home = temp_root / ".codex"
            local_agents = codex_home / "agents"
            self._copy_portable_repo(repo_root)
            local_agents.mkdir(parents=True)

            before_guidance = (repo_root / "codex" / "AGENTS.md").read_bytes()
            before_worker = (repo_root / "codex" / "agents" / "worker.toml").read_bytes()
            (codex_home / "AGENTS.md").write_text("new guidance\n", encoding="utf-8")
            shutil.copy2(AGENT_ROOT / "worker.toml", local_agents / "worker.toml")

            result = self._run_bash_script(
                repo_root, "sync-from-local.sh", codex_home, check=False
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("explorer.toml", result.stderr)
            self.assertEqual(
                (repo_root / "codex" / "AGENTS.md").read_bytes(), before_guidance
            )
            self.assertEqual(
                (repo_root / "codex" / "agents" / "worker.toml").read_bytes(),
                before_worker,
            )


if __name__ == "__main__":
    unittest.main()
