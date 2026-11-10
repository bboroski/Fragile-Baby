# MCST LCC toolchain and build workflow

## Toolchain boundary

Fragile-Baby does not implement an E2K machine-code backend. It delegates target code generation to the platform compiler supplied for the installed Elbrus Linux/SDK environment. MCST's programming guide documents native C/C++ builds through `lcc`; on the native platform, `gcc` and `g++` are documented aliases for the LCC C and C++ modes. Do not assume that an arbitrary host GCC binary targets e2k.

References:
- [MCST programming guide — compiler options and platform recognition](https://mcst.ru/doc/elbrus_prog/elbrus-prog-1.2_2024-02-28.pdf)
- [MCST open-source sources and patches](https://www.mcst.ru/sources)
- [MCST QEMU-e2k source announcement, 25 December 2025](https://www.mcst.ru/2025-12-25_qemu-e2k)

## Verify the compiler first

On a native Elbrus Linux system with the MCST toolchain installed:

```sh
python3 scripts/e2k-doctor.py
```

Or specify the compiler explicitly:

```sh
E2K_CC=/opt/mcst/bin/lcc python3 scripts/e2k-doctor.py
```

The doctor asks the selected compiler for predefined macros and requires `__e2k__`. A successful check proves target-family recognition only; it does not prove that the sysroot, linker, runtime libraries or target hardware are correct.

## CMake target build

```sh
cmake -S . -B build-e2k \
  -DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/e2k-linux.cmake \
  -DE2K_CC=/path/to/lcc \
  -DE2K_SYSROOT=/path/to/e2k/sysroot \
  -DFB_E2K_GENERATION=6 \
  -DFB_E2K_ADDRESS_MODEL=64
cmake --build build-e2k --parallel
```

- `E2K_CC` is the actual MCST LCC executable or a vendor-provided wrapper whose output has been verified to define `__e2k__`.
- `E2K_SYSROOT` is optional for a native installation and should point to a matching target root when cross-building.
- `FB_E2K_GENERATION` is 0 (unknown) or 1…7.
- `FB_E2K_ADDRESS_MODEL` is 32, 64 or 128; 64 is the default. The vendor guide documents `-m32`, `-m64` and `-m128`. The 128-bit pointer mode is a distinct protected-addressing model and must only be selected with a matching ABI/sysroot and application validation.

The toolchain checks `__e2k__` during CMake configure. If the compiler does not expose that target macro, configuration fails rather than quietly producing a host binary.

## Optimization policy

The MCST guide documents LCC optimization levels `-O0` through `-O4`. In general:

- Start with `-O0 -g` for debugging and source correspondence.
- Compare `-O2` and `-O3` using a representative target workload before selecting a release profile.
- Treat `-O4` as an experimental setting: the vendor guide warns that it can improve or degrade performance.
- LCC-specific profile generation/use and whole-program options have compatibility constraints. In particular, `-fwhole` and `-fwhole-shared` have different PIE/PIC and shared-library requirements; do not inject them as global flags without separating executable and shared-library targets.
- Preserve precise floating-point semantics unless the application explicitly accepts a different numerical contract.

Fragile-Baby intentionally does not hard-code speculative `-mcpu`, vector, scheduling, inline-assembly or PMU flags. The E2K compiler is responsible for instruction selection and scheduling; architecture-specific tuning must follow the installed LCC documentation and measured workload evidence.

## QEMU and execution testing

MCST announced publication of QEMU source with E2K support on 25 December 2025, enabling E2K Linux application binaries to run on x86-64 Linux hosts. Availability and packaging of a working `qemu-e2k` executable still depend on the installed distribution/build.

When a compatible runner is available, pass it as `E2K_QEMU` to CMake. Otherwise, build and archive target binaries, then run them on an actual Elbrus system. Do not report a cross-compile as a runtime test.

## Build stages

1. **Host tests:** validate the architecture-neutral C11 API on GCC/Clang.
2. **E2K configure:** verify LCC, target macro, address model and sysroot.
3. **E2K compile/link:** build the library and target smoke executable.
4. **Emulator test:** execute with a verified QEMU-e2k runner, where available.
5. **Silicon test:** run on the exact CPU model, OS build and board/system configuration.
6. **Performance qualification:** record compiler version, flags, CPU model, workload, thermal state, repetitions and perf/dprof evidence.

Only stages that have actually run should be marked complete.
