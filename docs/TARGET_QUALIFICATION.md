# Elbrus target profile and qualification

This repository is the architecture-specific compatibility workstream for Elbrus.
The profile format deliberately does not hard-code a CPU model, ABI, endianness,
compiler version, target triple or board revision. Those values must come from
the exact platform documentation and installed toolchain.

## Profile contract

`spec/target-profile.schema.json` defines the versioned
`fragile-baby.target-profile.v1` format. The example profile is intentionally
`profile_only`: unknown values remain null and the validator reports
`support_claim: not_established`.

Qualification is an evidence ladder:

| Level | Minimum evidence |
|---|---|
| `profile_only` | A structurally valid profile |
| `toolchain_detected` | Toolchain identity and ABI fields, plus toolchain evidence |
| `cross_compiled` | Toolchain and build evidence |
| `emulated` | Toolchain, build, emulator and test evidence |
| `hardware_validated` | Toolchain, build, hardware and test evidence, plus exact CPU model and board |

Every evidence record has a reference and SHA-256 digest. The validator checks
format and required evidence categories; it does not fetch or authenticate the
referenced artifacts.

## Run

```bash
python -m unittest discover -s tests
python tools/validate_target_profile.py spec/target-profile.example.json
python tools/validate_target_profile.py --self-test
```

## Implementation sequence

1. Record exact CPU model, board revision and vendor toolchain provenance.
2. Confirm target triple, sysroot, pointer width, endianness, calling convention
   and stack alignment from primary platform documentation.
3. Add the cross-compiler profile and linker configuration; keep host builds separate.
4. Cross-compile a minimal diagnostic, retain the binary, map and compiler logs.
5. Add emulator evidence only when a compatible emulator is available.
6. Promote to hardware-validated only with repeatable test logs from the named device.

A profile that passes host-side validation is not proof of a successful cross-build,
instruction-set support, kernel boot, driver operation or production readiness.
