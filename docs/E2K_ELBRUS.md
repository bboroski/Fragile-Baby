# E2K / Elbrus platform workstream

## Scope and current implementation status

This repository now carries the shared E2K Linux target contract, ELF64 little-endian machine identity (`EM_MCST_ELBRUS=175`), ISA matrix, MCST LCC CMake toolchain and references required by the other ecosystem components.

**Status: architecture profile and integration planning only.** This repository does not yet contain a firmware module, bootloader, kernel image, board-support package, native executable or E2K runtime. No Elbrus boot or hardware support is claimed here.

## Required implementation sequence

1. Bind exact processor model, stepping and Elbrus Linux release to a supported LCC SDK target.
2. Add a platform-specific implementation only when a published board interface or reviewed hardware specification exists.
3. Keep machine/ISA detection separate from optional performance counters, thermal sensors and clock policy.
4. Execute the full host and target test suites on native E2K hardware or an approved Elbrus Linux runner.
5. For bare-metal work, document the PNS image contract and prove the entry, memory, interrupt and device path independently. The general-purpose `qemu-e2k` user emulator is not a firmware/system emulator.

## Deployment boundary

The currently supported shared userspace route is MCST PNS → Elbrus Linux → E2K-native application. It is not a replacement for PNS, and it does not establish arbitrary third-party bare-metal kernel loading.

## References

- [Shared E2K target profile](platforms/e2k/target.json)
- [Shared MCST LCC CMake toolchain](cmake/toolchains/e2k-linux-lcc.cmake)
- [E2K profile and qualification notes](platforms/e2k/README.md)
- [MCST developer downloads](https://dev.mcst.ru/download/)
- [MCST SDK](https://www.mcst.ru/SDK)
- [MCST PNS](https://www.mcst.ru/boot)
