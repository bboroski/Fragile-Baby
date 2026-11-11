from __future__ import annotations
import unittest
from tools.evidence_advisor import analyze_matrix

BASE = {
    "schema_version": "fragile-baby.e2k-evidence.v1",
    "architecture": "E2K",
    "maturity": "architecture-proposal",
    "target_identity": {"cpu_model": None, "stepping": None, "board_revision": None, "toolchain": None},
    "stages": [
        {"stage": name, "status": "not-tested", "evidence": [], "toolchain_fingerprint": None}
        for name in ("host", "cross-build", "emulator", "physical-target")
    ],
    "limitations": []
}

class EvidenceAdvisorTests(unittest.TestCase):
    def test_empty_matrix_recommends_host_stage(self):
        report = analyze_matrix(BASE)
        self.assertTrue(report["valid"])
        self.assertEqual(report["coverage_percent"], 0)
        self.assertEqual(report["next_stage"], "host")
        self.assertIn("run the host", report["next_action"])

    def test_host_pass_does_not_promote_to_emulator(self):
        data = {**BASE, "maturity": "emulator-observed"}
        data["stages"] = [dict(item) for item in BASE["stages"]]
        data["stages"][0]["status"] = "passed"
        data["stages"][0]["evidence"] = ["host-ci://run/1"]
        report = analyze_matrix(data)
        self.assertEqual(report["coverage_percent"], 25)
        self.assertFalse(report["maturity_consistent"])
        self.assertEqual(report["next_stage"], "cross-build")

    def test_failed_stage_gets_specific_recovery_action(self):
        data = {**BASE, "stages": [dict(item) for item in BASE["stages"]]}
        data["stages"][0]["status"] = "failed"
        report = analyze_matrix(data)
        self.assertIn("investigate the host failure", report["next_action"])

    def test_unknown_is_not_passed(self):
        data = {**BASE, "stages": [dict(item) for item in BASE["stages"]]}
        data["stages"][0]["status"] = "unknown"
        report = analyze_matrix(data)
        self.assertEqual(report["coverage_percent"], 0)
        self.assertIn("unknown is not a pass", report["next_action"])

    def test_physical_claim_requires_identity_and_evidence(self):
        data = {**BASE, "maturity": "hardware-qualified", "stages": [dict(item) for item in BASE["stages"]]}
        for item in data["stages"]:
            item["status"] = "passed"
        report = analyze_matrix(data)
        self.assertTrue(report["maturity_consistent"])
        self.assertFalse(report["target_identity_complete"])
        self.assertTrue(any("target identity is incomplete" in warning for warning in report["warnings"]))
        self.assertTrue(any("without traceable evidence" in warning for warning in report["warnings"]))

    def test_invalid_schema_is_rejected(self):
        report = analyze_matrix({"architecture": "x86"})
        self.assertFalse(report["valid"])
        self.assertGreater(len(report["errors"]), 0)

if __name__ == "__main__":
    unittest.main()
