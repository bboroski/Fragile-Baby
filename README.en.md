<h1 align="center">Fragile-Baby</h1>
<p align="center"><strong>Elbrus Architecture &amp; Platform Qualification Workstream</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-ARCHITECTURE%20PROPOSAL-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/TARGET-ELBRUS%20%2F%20E2K-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/LICENSE-NOT%20DECLARED-FFD600?style=for-the-badge&labelColor=111111"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

---

**Fragile-Baby is a dedicated engineering workstream for Elbrus/E2K architecture research and verifiable processor-platform enablement.** Its purpose is to define exact ABI, toolchain, memory-map, and boot contracts before any compatibility claim is made.

## Current status

<badge>ARCHITECTURE PROPOSAL</badge>

The repository currently contains an architecture proposal and integration-reference material. There is no verified target implementation, proven boot path, or hardware qualification. No Elbrus CPU model or board is declared supported.

## Engineering scope

- Target-specific ABI and toolchain profiles.
- Image-format, memory-map, address-range, and alignment validation.
- Linker-layout and section checks.
- Versioned manifests for CPU/SoC, stepping, board revision, and toolchain.
- Reproducible evidence matrix for host, cross-build, emulator, and physical target.
- Narrow platform interface with explicit capability gates.

## Qualification contract

| Layer | Required evidence |
|---|---|
| CPU | Exact model, stepping, and available ISA/privilege features |
| Board | Revision, memory map, MMIO, and DMA windows |
| Toolchain | Compiler, binutils/linker, ABI, and startup objects |
| Image | Format, sections, alignment, checksum, and address bounds |
| Emulator | Specific emulator, version, and reproducible results |
| Hardware | Physical boot, serial/diagnostic output, and test evidence |

Host tests verify software invariants only. They do not replace cross-build, emulation, or physical-hardware validation. Elbrus properties must not be inferred from ARM, x86, or RISC-V; each port must use documentation for the exact CPU and platform.

## Governance and boundaries

Before implementation, define domain ownership, supported CPU variants, public interfaces, threat model, build/test strategy, license, and dependency direction. New integrations must be versioned, independently testable, and reversible.

Documentation: [engineering integration](docs/REAPER_DOMAIN_INTEGRATION.md) · [boundary and invariant profile](docs/CLOSED_DOMAIN_METRIC_INTEGRATION.md) · [canonical CDM-1 specification in SAMBU](https://github.com/bboroski/SAMBU/blob/main/docs/CLOSED_DOMAIN_METRIC.md).

## Ecosystem and license

Related projects: [Kloz](https://github.com/bboroski/Kloz), [ReaperCripple](https://github.com/bboroski/ReaperCripple), [NUN](https://github.com/bboroski/NUN), [NUNLauncher](https://github.com/bboroski/NUNLauncher), and [Klipot](https://github.com/bboroski/Klipot).

No <code>LICENSE</code> file is present; no license is declared. Define the terms before public distribution.

---

**Built with love for open engineering and people.**