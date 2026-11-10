import unittest

from tools.validate_target_profile import (
    ProfileError, _fixture, validate_profile,
)


class TargetProfileTests(unittest.TestCase):
    def test_profile_only_does_not_claim_support(self):
        report = validate_profile(_fixture())
        self.assertEqual(report["qualification_level"], "profile_only")
        self.assertEqual(report["support_claim"], "not_established")
        self.assertFalse(report["toolchain_configured"])
        self.assertFalse(report["abi_configured"])

    def test_each_qualification_level_has_its_evidence_floor(self):
        for level in ("profile_only", "toolchain_detected", "cross_compiled",
                      "emulated", "hardware_validated"):
            with self.subTest(level=level):
                result = validate_profile(_fixture(level))
                self.assertEqual(result["qualification_level"], level)

    def test_cross_compile_requires_build_evidence(self):
        profile = _fixture("cross_compiled")
        profile["qualification"]["evidence"] = [
            item for item in profile["qualification"]["evidence"]
            if item["kind"] != "build"
        ]
        with self.assertRaises(ProfileError):
            validate_profile(profile)

    def test_hardware_claim_requires_exact_target_identity(self):
        profile = _fixture("hardware_validated")
        profile["target"]["board"] = None
        with self.assertRaises(ProfileError):
            validate_profile(profile)

    def test_abi_alignment_must_be_power_of_two(self):
        profile = _fixture("toolchain_detected")
        profile["abi"]["stack_alignment_bytes"] = 24
        with self.assertRaises(ProfileError):
            validate_profile(profile)

    def test_boolean_is_not_accepted_as_pointer_width(self):
        profile = _fixture("toolchain_detected")
        profile["abi"]["pointer_width_bits"] = True
        with self.assertRaises(ProfileError):
            validate_profile(profile)

    def test_architecture_and_evidence_hash_are_validated(self):
        profile = _fixture()
        profile["architecture"] = "x86_64"
        with self.assertRaises(ProfileError):
            validate_profile(profile)
        profile = _fixture("toolchain_detected")
        profile["qualification"]["evidence"][0]["sha256"] = "bad"
        with self.assertRaises(ProfileError):
            validate_profile(profile)


if __name__ == "__main__":
    unittest.main()
