# Elbrus / E2K Qualification Plan

**Status:** planned engineering work; no target has been certified by this repository.

## 1. Identify the actual target

Record the exact CPU model, board vendor, board revision, memory configuration and firmware version. Do not treat the name Elbrus alone as a sufficient hardware identity. Keep one profile per combination that materially changes the ABI, boot process or peripheral map.

## 2. Establish a reproducible toolchain

Record compiler name and full version, target triple, sysroot, linker and version, C library/runtime, assembler, build flags and source of the toolchain. Preserve the exact build command and hashes of toolchain artifacts where licensing permits.

Do not guess a target triple, linker script, compiler flag or vendor extension from an AI-generated answer. Confirm it against the toolchain actually installed and the matching vendor documentation.

## 3. Capture ABI facts

For each target profile, document calling convention, data model, pointer width, integer widths, endianness, alignment, stack direction and alignment, atomic support, exception/interrupt ABI and required runtime helpers. Derive values from authoritative toolchain documentation and compile-time probes.

## 4. Qualification layers

| Layer | Evidence required | What it proves |
|---|---|---|
| Metadata | Profile validator passes | Profile structure only |
| Host | Portable C11 tests pass on host | Host-side logic only |
| Cross compile | Target compiler builds probes and libraries | Compiler accepts the sources for the declared target |
| Link | Linker output and map are inspected | The selected objects and memory layout link |
| Emulator | Matching emulator executes test fixtures | Behavior within that emulator |
| Hardware | Tests on the exact board revision | Evidence for that hardware/software combination |

A successful earlier layer never implies that a later layer has passed.

## 5. Initial portable probes

Start with integer widths, structure layout, alignment, endianness, atomics, volatile access, monotonic clock behavior and CRC test vectors. Then qualify the Kloz platform boundary, CO lifecycle callbacks and SaintSI caller-supplied tick source. Only after these pass should ReaperCripple BSP and runtime stages be considered for the target.

## 6. Safety and release gate

Do not experiment with voltage, clock limits, undocumented registers, firmware flashing or bootloader changes during compiler qualification. Those require a separate board-specific procedure, recovery path and explicit operator authorization.

The status target-validated is allowed only with reproducible hardware logs, exact target identity, exact toolchain versions, build artifacts and passing test results. AI output, generated documentation and host-only CI are not hardware evidence.
