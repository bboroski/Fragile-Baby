# Architecture qualification model

Fragile-Baby is reserved for architecture-specific compatibility and qualification work. Its Elbrus target profile must remain explicit and evidence-driven; an architecture label alone is never a support claim.

## Target ownership

- Each target profile must declare the architecture variant, toolchain identity and version, target triple, ABI properties and enabled features.
- Unknown ABI/toolchain fields remain unknown; they must not be guessed from another CPU family.
- Build flags, linker scripts, sysroot, firmware assumptions and board revision belong to a versioned target profile, not scattered conditionals.
- Common runtime code must call explicit architecture adapters and must not infer support from the host build.

## Qualification ladder

A target progresses through distinct evidence states: profile-only, toolchain detected, cross-compiled, emulated and hardware-validated. Each promotion requires evidence artifacts with content hashes. Hardware validation additionally identifies the actual target and test results.

## Current scope

The repository is a qualification scaffold until its profile, compiler, sysroot, linker layout, emulator and target hardware are supplied and verified. The documentation does not assert that the current branch compiles or runs on Elbrus.
