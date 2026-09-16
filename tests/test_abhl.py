import unittest
from pathlib import Path

from abhl import compile_manifest, parse_file, validate

ROOT = Path(__file__).resolve().parents[1]


class ABHLTests(unittest.TestCase):
    def codes(self, example: str) -> set[str]:
        program = parse_file(ROOT / "examples" / example)
        return {d.code for d in validate(program)}

    def test_valid_ci_demo_compiles(self):
        p = parse_file(ROOT / "examples" / "ci_demo.abhl")
        self.assertEqual(validate(p), [])
        manifest = compile_manifest(p)
        self.assertIn("dependency", manifest["scopes"])
        self.assertIn("integration", manifest["scopes"])
        self.assertEqual(manifest["handoffs"]["integration_handoff"]["authority"], "none")

    def test_cross_scope_ground_mutation_is_rejected(self):
        self.assertIn("E702", self.codes("attack_remote_mutation.abhl"))

    def test_handoff_cannot_transfer_authority(self):
        self.assertIn("E201", self.codes("attack_authority_handoff.abhl"))

    def test_widening_cannot_add_privilege(self):
        self.assertIn("E602", self.codes("attack_widen_privilege.abhl"))


if __name__ == "__main__":
    unittest.main()
