import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_ROOT = REPO_ROOT / "codex"
SHARED_GUIDANCE = CODEX_ROOT / "AGENTS.md"


class PortableConfigTests(unittest.TestCase):
    def test_shared_guidance_is_the_only_installable_config(self):
        installed_files = sorted(
            path.relative_to(CODEX_ROOT)
            for path in CODEX_ROOT.rglob("*")
            if path.is_file()
        )
        self.assertEqual(installed_files, [Path("AGENTS.md")])

    def test_readme_has_no_custom_agent_defaults(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("codex/agents", readme)
        self.assertNotIn("[agents]", readme)
        self.assertNotIn("default_subagent_", readme)

    @unittest.skipUnless(os.name == "posix", "requires a POSIX shell")
    def test_installer_removes_only_previously_managed_agents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / ".codex"
            agent_root = codex_home / "agents"
            agent_root.mkdir(parents=True)

            managed_agent = agent_root / "worker.toml"
            unmanaged_agent = agent_root / "personal.toml"
            managed_agent.write_text("managed\n", encoding="utf-8")
            unmanaged_agent.write_text("personal\n", encoding="utf-8")
            state_path = codex_home / ".portable-config-agent-files"
            state_path.write_text("worker.toml\n../outside.toml\n", encoding="utf-8")
            config_path = codex_home / "config.toml"
            config_path.write_text("sentinel = true\n", encoding="utf-8")

            environment = os.environ.copy()
            environment["CODEX_HOME"] = str(codex_home)
            subprocess.run(
                ["bash", str(REPO_ROOT / "scripts" / "install.sh")],
                cwd=REPO_ROOT,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                (codex_home / "AGENTS.md").read_bytes(),
                SHARED_GUIDANCE.read_bytes(),
            )
            self.assertFalse(managed_agent.exists())
            self.assertEqual(unmanaged_agent.read_text(encoding="utf-8"), "personal\n")
            self.assertFalse(state_path.exists())
            self.assertEqual(config_path.read_text(encoding="utf-8"), "sentinel = true\n")


if __name__ == "__main__":
    unittest.main()
