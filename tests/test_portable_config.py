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
    "explorer": ("gpt-6-luna", "max", "workspace-write"),
    "worker": ("gpt-6-sol", "medium", "workspace-write"),
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
                Path("config.shared.toml"),
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

    def test_shared_defaults(self):
        shared = tomllib.loads((CODEX_ROOT / "config.shared.toml").read_text())
        self.assertEqual(shared, {
            "model": "gpt-6-astra", "model_reasoning_effort": "xhigh",
            "agents": {"max_concurrent_threads_per_session": 4,
                       "default_subagent_model": "gpt-6-sol",
                       "default_subagent_reasoning_effort": "medium"},
        })

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
            config = tomllib.loads(config_path.read_text(encoding="utf-8"))
            self.assertTrue(config.pop("sentinel"))
            self.assertEqual(config, tomllib.loads((CODEX_ROOT / "config.shared.toml").read_text()))

    def _config_case(self, local, shared=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        repo, home = root / "repo", root / "home"
        self._copy_portable_repo(repo)
        shutil.copytree(CODEX_ROOT, home)
        (home / "config.toml").write_text(local, encoding="utf-8")
        if shared is not None:
            (repo / "codex/config.shared.toml").write_text(shared, encoding="utf-8")
        return repo, home

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_merge_preserves_comments_unmanaged_and_is_idempotent(self):
        local = ('# personal\nmodel = "old" # model note\n'
                 'model_reasoning_effort = "low" # retained\n'
                 '[agents] # agents note\ncustom = true # custom note\n'
                 'default_subagent_model = "old-sub" # sub note\n'
                 '[projects."/private/work"]\ntrust_level = "trusted" # trust note\n')
        repo, home = self._config_case(local, 'model = "new"\n[agents]\ndefault_subagent_model = "new-sub"\n')
        self._run_bash_script(repo, "install.sh", home)
        first = (home / "config.toml").read_text()
        self._run_bash_script(repo, "install.sh", home)
        self.assertEqual(first, (home / "config.toml").read_text())
        for comment in ("# personal", "# model note", "# retained", "# agents note", "# custom note", "# sub note", "# trust note"):
            self.assertIn(comment, first)
        data = tomllib.loads(first)
        self.assertEqual(data["model"], "new")
        self.assertEqual(data["model_reasoning_effort"], "low")
        self.assertEqual(data["agents"], {"custom": True, "default_subagent_model": "new-sub"})
        self.assertEqual(data["projects"]["/private/work"]["trust_level"], "trusted")

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_extract_only_present_whitelisted_values(self):
        local = ('model = "future-model" # private comment\nsecret = "token"\n'
                 '[agents]\nmax_concurrent_threads_per_session = 9\n'
                 '[agents.personal]\nmodel = "private"\n[plugins]\nenabled = true\n')
        repo, home = self._config_case(local)
        self._run_bash_script(repo, "sync-from-local.sh", home)
        shared = (repo / "codex/config.shared.toml").read_text()
        self.assertEqual(tomllib.loads(shared), {"model": "future-model", "agents": {"max_concurrent_threads_per_session": 9}})
        self.assertNotIn("private", shared)
        self.assertNotIn("token", shared)
        self.assertEqual((home / "config.toml").read_text(), local)
        self._run_bash_script(repo, "sync-from-local.sh", home)
        self.assertEqual((repo / "codex/config.shared.toml").read_text(), shared)

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_invalid_toml_and_unknown_shared_reject_before_writes(self):
        cases = [
            ('model = "one"\nmodel = "two"\n', None),
            ('model = [\n', None),
            ('model = "local"\n', 'model = "one"\nmodel = "two"\n'),
            ('model = "local"\n', '[plugins]\nenabled = true\n'),
            ('model = "local"\n', '[agents.personal]\nmodel = "private"\n'),
        ]
        for local, shared in cases:
            for script in ("install.sh", "sync-from-local.sh"):
                with self.subTest(local=local, shared=shared, script=script):
                    repo, home = self._config_case(local, shared)
                    (home / "AGENTS.md").write_text("changed local guidance\n")
                    before = {path: path.read_bytes() for base in (repo / "codex", home) for path in base.rglob("*") if path.is_file()}
                    result = self._run_bash_script(repo, script, home, check=False)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual({path: path.read_bytes() for path in before}, before)

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_empty_shared_retains_all_local_values(self):
        local = 'model = "retained" # local\n[agents]\ndefault_subagent_model = "retained-sub"\n'
        repo, home = self._config_case(local, "# no declarations\n")
        self._run_bash_script(repo, "install.sh", home)
        self.assertEqual((home / "config.toml").read_text(), local)

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_missing_local_config_can_install_but_sync_rejects(self):
        for script in ("install.sh", "sync-from-local.sh"):
            with self.subTest(script=script):
                repo, home = self._config_case("")
                (home / "config.toml").unlink()
                before = (repo / "codex/config.shared.toml").read_bytes()
                result = self._run_bash_script(repo, script, home, check=False)
                if script == "install.sh":
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(tomllib.loads((home / "config.toml").read_text()), tomllib.loads((CODEX_ROOT / "config.shared.toml").read_text()))
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("config.toml", result.stderr)
                    self.assertEqual((repo / "codex/config.shared.toml").read_bytes(), before)

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
            (codex_home / "config.toml").write_text("", encoding="utf-8")

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
            (codex_home / "config.toml").write_text("", encoding="utf-8")
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
