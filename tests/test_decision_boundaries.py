import json
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_ROOT = REPO_ROOT / "codex"
AGENTS_PATH = CODEX_ROOT / "AGENTS.md"
AGENT_ROOT = CODEX_ROOT / "agents"
CASES_PATH = Path(__file__).with_name("decision_boundary_cases.json")


class AgentFileContractTests(unittest.TestCase):
    def test_every_agent_toml_parses_and_has_required_fields(self):
        agent_paths = sorted(AGENT_ROOT.glob("*.toml"))
        self.assertTrue(agent_paths)

        for agent_path in agent_paths:
            with self.subTest(agent=agent_path.name):
                data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
                for key in ("name", "description", "developer_instructions"):
                    self.assertIsInstance(data.get(key), str)
                    self.assertTrue(data[key].strip())

    def test_global_guidance_keeps_semantic_authority_distinct(self):
        guidance = AGENTS_PATH.read_text(encoding="utf-8")

        for phrase in (
            "Decision Authority",
            "`LOCKED` product meaning",
            "`OPEN` decisions",
            "evidence-testable `ASSUMPTION`s",
            "Neither chooses replacement product meaning",
            "A child finding does not change the governing contract",
            "`REJECT_AS_ALTERNATIVE_OR_OUT_OF_SCOPE`",
            "`POLICY_BLOCKED`",
            "no product-semantic change",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, guidance)

    def test_boundary_sensitive_agents_preserve_role_authority(self):
        reviewer = self._instructions("reviewer.toml")
        reasoner = self._instructions("decision_reasoner.toml")
        arbitrator = self._instructions("decision_arbitrator.toml")

        self.assertIn("do not act as the product owner", reviewer)
        for classification in (
            "Contract violation",
            "Implementation defect",
            "Residual risk",
            "Alternative",
            "Policy blocked",
        ):
            self.assertIn(classification, reviewer)
        self.assertIn(
            "the intended contract is unchanged but code or runtime behavior fails",
            reviewer,
        )
        self.assertIn("no semantic change", reviewer)

        for label in ("`LOCKED`", "`OPEN`", "`ASSUMPTION`s"):
            self.assertIn(label, reasoner)
            self.assertIn(label, arbitrator)
        self.assertIn("REQUEST_REOPENING", reasoner)
        self.assertIn("REQUEST_REOPENING", arbitrator)
        self.assertNotIn(
            "Arbitrate from evidence rather than the authority or stated preference",
            arbitrator,
        )

    def test_delegation_guidance_is_cost_weighted_and_nonduplicative(self):
        guidance = AGENTS_PATH.read_text(encoding="utf-8")

        for phrase in (
            "substantial practical work default to subagents",
            "exactly one least-expensive capable named subagent",
            "broad mapping, implementation, and lane-local validation",
            "before the parent performs it",
            "no safe independent lane exists",
            "delegation is unavailable",
            "Do not split coherent lanes merely to reach a cheaper model",
            "decoy delegation, duplicate parent work, or speculative fan-out",
            "Do not repeat completed lane work",
            "Steer or reassign an incomplete lane before taking it over",
            "compact self-contained packet",
            "role-configured model",
            "built-in `worker` fallback",
            'fork_turns = "none"',
            "Children do not delegate",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, guidance)

    def test_agent_models_use_allowlist_and_worker_contracts(self):
        allowed_models = {"gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"}
        agent_paths = sorted(AGENT_ROOT.glob("*.toml"))
        self.assertTrue(agent_paths)
        for agent_path in agent_paths:
            with self.subTest(agent=agent_path.name):
                data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
                self.assertIn(data["model"], allowed_models)

        for name, expected_model in (
            ("focused_worker.toml", "gpt-5.6-luna"),
            ("verification_worker.toml", "gpt-5.6-luna"),
            ("worker.toml", "gpt-5.6-terra"),
        ):
            with self.subTest(agent=name):
                data = tomllib.loads((AGENT_ROOT / name).read_text(encoding="utf-8"))
                self.assertEqual(data["model"], expected_model)
                self.assertEqual(data["model_reasoning_effort"], "medium")

        worker = tomllib.loads((AGENT_ROOT / "worker.toml").read_text(encoding="utf-8"))
        self.assertEqual(worker["name"], "worker")
        self.assertIn("substantial cohesive repository lane", worker["description"])
        self.assertEqual(worker["model"], "gpt-5.6-terra")
        self.assertEqual(worker["model_reasoning_effort"], "medium")
        self.assertEqual(worker["sandbox_mode"], "workspace-write")
        for marker in (
            "substantial cohesive repository lane",
            "bounded multi-file implementation and focused validation lane",
            "no narrower custom role fits",
            "Do not spawn or delegate",
            "explicitly assigned write boundary",
            "preserve unrelated edits",
            "discovery, implementation, and focused validation",
            "product, architecture, API, schema, security, permission, or public-contract decisions",
            "Escalate material semantic decisions",
            "scoped diff",
            "Changes, Validation, Remaining Risk",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, worker["developer_instructions"])

    def _instructions(self, name):
        data = tomllib.loads((AGENT_ROOT / name).read_text(encoding="utf-8"))
        return data["developer_instructions"]


class DecisionBoundaryCaseTests(unittest.TestCase):
    def test_representative_cases_keep_expected_dispositions(self):
        payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in payload["cases"]}
        guidance = AGENTS_PATH.read_text(encoding="utf-8")

        self.assertEqual(payload["version"], 1)
        self.assertEqual(
            set(cases),
            {
                "safer_alternative_changes_locked_meaning",
                "implementation_fails_locked_boundary",
                "policy_denial_without_equivalent_path",
            },
        )
        self.assertEqual(
            cases["safer_alternative_changes_locked_meaning"],
            {
                "id": "safer_alternative_changes_locked_meaning",
                "situation": "A reviewer proposes a narrower trust boundary only because it is safer, even though the user approved the current broader boundary.",
                "classification": "Alternative",
                "gate": "PASS",
                "disposition": "REJECT_AS_ALTERNATIVE_OR_OUT_OF_SCOPE",
                "decision_complete": False,
                "semantic_delta": True,
                "auto_fix": False,
            },
        )
        self.assertEqual(
            cases["implementation_fails_locked_boundary"]["classification"],
            "Implementation defect",
        )
        self.assertEqual(
            cases["implementation_fails_locked_boundary"]["disposition"],
            "FIX_WITHIN_CONTRACT",
        )
        self.assertTrue(
            cases["implementation_fails_locked_boundary"]["decision_complete"]
        )
        self.assertFalse(
            cases["implementation_fails_locked_boundary"]["semantic_delta"]
        )
        self.assertTrue(cases["implementation_fails_locked_boundary"]["auto_fix"])
        self.assertEqual(
            cases["policy_denial_without_equivalent_path"]["classification"],
            "Policy blocked",
        )
        self.assertEqual(
            cases["policy_denial_without_equivalent_path"]["disposition"],
            "POLICY_BLOCKED",
        )
        self.assertFalse(
            cases["policy_denial_without_equivalent_path"]["decision_complete"]
        )
        self.assertFalse(cases["policy_denial_without_equivalent_path"]["auto_fix"])

        for case in cases.values():
            with self.subTest(case=case["id"]):
                self.assertIn(f'`{case["disposition"]}`', guidance)
                if case["auto_fix"]:
                    self.assertIn(
                        case["classification"],
                        {"Contract violation", "Implementation defect"},
                    )
                    self.assertTrue(case["decision_complete"])
                    self.assertFalse(case["semantic_delta"])


if __name__ == "__main__":
    unittest.main()
