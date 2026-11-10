from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_toolchain_profile import validate_profile  # noqa: E402


class ToolchainProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        with (ROOT / "profiles" / "elbrus.template.json").open(encoding="utf-8") as stream:
            self.profile = json.load(stream)

    def test_unverified_template_is_valid(self) -> None:
        validate_profile(self.profile)

    def test_target_validation_requires_hardware_evidence(self) -> None:
        candidate = json.loads(json.dumps(self.profile))
        candidate["status"] = "target-validated"
        with self.assertRaises(ValueError):
            validate_profile(candidate)

    def test_rejects_wrong_architecture_family(self) -> None:
        candidate = json.loads(json.dumps(self.profile))
        candidate["architecture"]["family"] = "x86_64"
        with self.assertRaises(ValueError):
            validate_profile(candidate)


if __name__ == "__main__":
    unittest.main()
