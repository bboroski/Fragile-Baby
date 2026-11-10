# Elbrus / E2K Qualification Framework

Fragile-Baby is the target-enablement and qualification layer for Elbrus/E2K
systems. The current implementation is a portable qualification-state API; it
does **not** claim that a specific Elbrus CPU, compiler, ABI, board, or sysroot
has been tested.

## Ambiguity converted into gates

| Unknown | Feature | Safe behavior |
|---|---|---|
| CPU model/revision | Explicit target profile | No CPU feature is assumed |
| Compiler executable/version | Toolchain preflight evidence | No compiler command is guessed |
| Sysroot and runtime ABI | ABI layout and link probes | Cross-build remains unqualified |
| Endianness and pointer model | Required profile fields | No data layout is inferred |
| Board, peripherals, firmware | Hardware bring-up evidence | Host tests cannot qualify a board |
| Performance/thermal/power envelope | Measurement record | No clock or voltage policy is applied |

## Executable API

`fb_elbrus_evaluate()` produces the next gate:

`needs_configuration → toolchain_pending → abi_pending → hardware_pending → qualified`

Any failed gate becomes a corresponding `*_blocked` state. A PASS or FAIL
must include a retained evidence reference. An absent value is never converted
to a default. A qualified result therefore means that the caller supplied
evidence for all three gates; it is not a cryptographic attestation.

## Required target evidence

1. Exact CPU model/revision and board identity.
2. Operator-supplied compiler path, version output, target triple, and sysroot.
3. ABI probes for widths, alignment, structure layout, calling convention, and
   link/runtime behavior.
4. Target-side bring-up report covering serial output, memory map, interrupts,
   timers, and the peripherals claimed by that profile.
5. Reproducible build logs and test artifact references.

The C11 host test validates only the qualification state machine. It does not
build an E2K binary or test physical hardware.
