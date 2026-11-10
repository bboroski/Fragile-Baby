# Fragile-Baby

**Elbrus / E2K Target Qualification Framework**

<p><img src="assets/duck-ui/duck-mark.svg" alt="Duck mark" width="88" /></p>

Fragile-Baby turns missing information about Elbrus systems into explicit target-profile fields, compiler and ABI probes, hardware evidence gates, and reproducible qualification reports.

## Implemented host-side features

- Versioned E2K profile model with explicit CPU model, compiler, compiler version, sysroot, ABI, pointer width, and endianness.
- Separate toolchain, ABI, and hardware bring-up evidence states.
- PASS and FAIL evidence must reference retained reports.
- The fb_elbrus_evaluate API returns a deterministic qualification stage and refuses to infer missing configuration.
- CMake host build, unit tests, and a one-command check entrypoint.

## Quick start

    cmake -S . -B build -DBUILD_TESTING=ON
    cmake --build build
    ctest --test-dir build --output-on-failure
    python one.py check

## Qualification sequence

NEEDS_CONFIGURATION → TOOLCHAIN_PENDING → ABI_PENDING → HARDWARE_PENDING → QUALIFIED

A failed toolchain, ABI, or hardware gate moves the profile into its corresponding blocked state. An incomplete profile remains unqualified.

## Elbrus toolchain

cmake/toolchains/elbrus-e2k.cmake requires the caller to supply the verified compiler executable and sysroot via FRAGILE_BABY_E2K_C_COMPILER and FRAGILE_BABY_E2K_SYSROOT. It deliberately does not guess compiler names, target triples, CPU variants, or ABI details.

## Evidence boundary

The current test suite runs on a host C11 compiler and validates only the qualification state machine. No actual E2K compiler, sysroot, CPU, board, or peripheral has been qualified by this host test. The profile starts with unknown target facts, and hardware support remains pending until target-side evidence is supplied.

See docs/ELBRUS_QUALIFICATION.md and ecosystem/uncertainty.json.

## License

Not yet selected. Distribution requires an explicit owner decision and a complete license text.
