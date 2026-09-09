import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENT_ROOT = REPO_ROOT / "codex" / "agents"
REQUIRED_STRING_FIELDS = (
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
    "developer_instructions",
)
ALLOWED_MODELS = {"gpt-6-astra", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"}
ALLOWED_REASONING_EFFORTS = {"medium", "high", "xhigh", "max"}
ALLOWED_SANDBOX_MODES = {"read-only", "workspace-write"}
ROLE_CONTRACTS = {
    "code_mapper": ("gpt-5.6-luna", "max"),
    "decision_reviewer": ("gpt-5.6-sol", "high"),
    "docs_researcher": ("gpt-5.6-luna", "high"),
    "explorer": ("gpt-5.6-luna", "high"),
    "frontend_worker": ("gpt-6-astra", "high"),
    "reviewer": ("gpt-5.6-sol", "high"),
    "routine_worker": ("gpt-5.6-luna", "medium"),
    "verification_worker": ("gpt-5.6-luna", "medium"),
    "worker": ("gpt-5.6-luna", "max"),
}


class PortableConfigTests(unittest.TestCase):
    def test_agent_tomls_have_portable_structure(self):
        agent_paths = sorted(AGENT_ROOT.glob("*.toml"))
        self.assertTrue(agent_paths)
        names = set()

        for agent_path in agent_paths:
            with self.subTest(agent=agent_path.name):
                data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
                for field in REQUIRED_STRING_FIELDS:
                    self.assertIsInstance(data.get(field), str)
                    self.assertTrue(data[field].strip())

                self.assertEqual(agent_path.stem, data["name"])
                self.assertNotIn(data["name"], names)
                names.add(data["name"])
                self.assertIn(data["model"], ALLOWED_MODELS)
                self.assertIn(
                    data["model_reasoning_effort"], ALLOWED_REASONING_EFFORTS
                )
                self.assertIn(data["sandbox_mode"], ALLOWED_SANDBOX_MODES)

        self.assertEqual(names, set(ROLE_CONTRACTS))

    def test_roles_keep_cost_routing_contracts(self):
        for name, (model, reasoning_effort) in ROLE_CONTRACTS.items():
            with self.subTest(agent=name):
                data = tomllib.loads(
                    (AGENT_ROOT / f"{name}.toml").read_text(encoding="utf-8")
                )
                self.assertEqual(data["model"], model)
                self.assertEqual(data["model_reasoning_effort"], reasoning_effort)


if __name__ == "__main__":
    unittest.main()
