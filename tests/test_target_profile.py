import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_target_profile import build_compile_argv, validate_profile  # noqa: E402


class ElbrusProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(
            (ROOT / "profiles" / "elbrus-reference.json").read_text(encoding="utf-8")
        )

    def test_template_is_valid_without_claiming_support(self):
        self.assertEqual(validate_profile(self.profile), [])
        self.assertFalse(self.profile["verification"]["hardware"])

    def test_strict_mode_requires_compiler_and_target(self):
        errors = validate_profile(self.profile, require_toolchain=True)
        self.assertTrue(any("compiler" in item for item in errors))
        self.assertTrue(any("target_triple" in item for item in errors))

    def test_command_is_composed_without_shell(self):
        self.profile["toolchain"]["compiler"] = "ccache e2k-compiler"
        self.profile["target_triple"] = "vendor-configured-target"
        self.profile["toolchain"]["flags"] = ["-O2", "-fno-common"]
        argv = build_compile_argv(self.profile, "unit.c", "unit.o")
        self.assertEqual(argv, [
            "ccache", "e2k-compiler", "-O2", "-fno-common",
            "-c", "unit.c", "-o", "unit.o",
        ])

    def test_duplicate_flags_rejected(self):
        self.profile["toolchain"]["flags"] = ["-O2", "-O2"]
        self.assertTrue(any("duplicates" in item for item in validate_profile(self.profile)))

    def test_unknown_architecture_rejected(self):
        self.profile["architecture"] = "x86_64"
        self.assertTrue(any("architecture" in item for item in validate_profile(self.profile)))


if __name__ == "__main__":
    unittest.main()
