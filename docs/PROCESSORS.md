# Elbrus processor and OS compatibility matrix

Fragile-Baby treats the E2K instruction-set generation, the physical processor model, and the installed operating-system/compiler release as separate fields. A model name alone is not enough to select compiler flags or promise runtime compatibility.

## Publicly documented generation families

| ISA generation | Processor models listed by MCST | Integration rule |
|---|---|---|
| e2k-v1 | Elbrus (first generation) | Legacy target; verify the exact compiler and OS package set |
| e2k-v2 | Elbrus-S, Elbrus-2C+ | Legacy target; verify the exact compiler and OS package set |
| e2k-v3 | Elbrus-4C | Use an SDK and OS release that explicitly supports v3 |
| e2k-v4 | Elbrus-8C, Elbrus-1C+, Elbrus-1CK | Use an SDK and OS release that explicitly supports v4 |
| e2k-v5 | Elbrus-8SV | Use an SDK and OS release that explicitly supports v5 |
| e2k-v6 | Elbrus-16C, Elbrus-12C, Elbrus-2C3 | Use an SDK and OS release that explicitly supports v6 |
| e2k-v7 | Elbrus-48C, Elbrus-8V7 | Use an SDK and OS release that explicitly supports v7 |

Sources: [MCST Elbrus Linux supported processor table](https://www.mcst.ru/elbrus_linux), [Elbrus processor identifiers](https://wiki.elbrus.ru/CPU_id).

The MCST OS page lists e2k-v7 for Elbrus-48C/8V7, v6 for 16C/12C/2C3, v5 for 8SV, v4 for 8C/1C+/1CK and v3 for 4C. It also lists the OS release ranges associated with those architecture families. These entries are a vendor compatibility reference, not a guarantee that a particular SDK, driver, firmware or package repository is available to every user.

## Build-time generation selection

Set `FB_E2K_GENERATION` to a value from 1 to 7 only when the exact target is known:

```sh
cmake -S . -B build-e2k \
  -DCMAKE_TOOLCHAIN_FILE=cmake/toolchains/e2k-linux.cmake \
  -DFB_E2K_GENERATION=6
```

Use `0` when the generation has not been established. Fragile-Baby does not infer a generation from CPU count, marketing name fragments, or undocumented compiler macros.

## Safe capability policy

- The presence of `__e2k__` confirms the compiler target family, not the exact chip stepping.
- A compiler target profile does not prove that every instruction or runtime library is available on every processor generation.
- PMU events, cache counters, thermal sensors and voltage controls are not assumed to exist or be readable from userspace.
- Kernel, firmware and board-specific features require their own validated drivers and permissions.
- Performance flags must be benchmarked per target generation and workload. Do not use one machine's profile as a universal tuning baseline.
