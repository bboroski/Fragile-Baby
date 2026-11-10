# Elbrus Domain Capabilities

Fragile-Baby is organized as an Elbrus/e2k architecture and toolchain-integration
workbench. The supplied biology and Reaper terminology is translated into
engineering profiles, target capability checks and controlled build evolution.

## Implemented functions

- **Endoskeletal replacement / bio-synthetic chassis:** `validate_profile`
  verifies the declared target ABI profile and capability inventory.
- **Neural node / distributed processing:** capability slots represent atomic
  operations, vector support, memory ordering and cache-coherency behavior.
- **Kinetic barrier / hull integrity:** architecture-specific validation gates
  keep unknown memory, privilege and interrupt properties explicitly unverified.
- **Core reconstruction / harvest cycles:** versioned target profiles and
  evidence flags support staged promotion and rollback planning.
- **Mass-effect physics:** any Eezo/field terminology is restricted to optional
  simulation or benchmark datasets, never processor specifications.
- **Toolchain pipeline:** `build_compile_argv` composes a compiler argument vector
  from an explicit user-supplied template and never uses shell execution.

## Usage

```sh
python tools/validate_target_profile.py
python -m unittest tests.test_target_profile
python tools/validate_target_profile.py --profile profiles/elbrus-reference.json \
  --source smoke.c --output smoke.o
```

Add the exact compiler command, target identifier, ABI properties and flags only
after they have been established for the relevant Elbrus toolchain distribution.
To actually run a cross-build, supply all required profile data and pass `--run`.

## Verification boundary

The checked-in profile is a research template: compiler, target triple, ABI facts,
emulator and hardware verification are intentionally unset. Passing profile
validation does not prove that an Elbrus compiler is installed or that any CPU
feature works. Target builds and hardware tests remain separate evidence gates.
