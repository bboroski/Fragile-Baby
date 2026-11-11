# Fragile-Baby
**Elbrus Architecture & Platform Qualification**

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md)

An engineering workstream for Elbrus/E2K research and verifiable platform qualification.

## Features
- CPU/SoC, stepping and ABI identity profiles.
- Toolchain, linker layout, image format and memory-map requirements.
- Versioned manifests for CPU, board revision and compiler toolchain.
- Evidence matrix for host, cross-build, emulator and physical target.

## Run and test
```bash
python3 tools/evidence_advisor.py
```

## Scope
No verified E2K target implementation, boot path or hardware qualification is present. Host tests do not prove Elbrus compatibility; parameters must not be inferred from another ISA.

## Project documentation
This project focuses on specifications and evidence matrices, not a GUI. No hardware screenshots are fabricated.

## Related
[Evidence advisor](docs/EVIDENCE_ADVISOR.md) · [NUN](https://github.com/bboroski/NUN) · [Hellduck](https://github.com/bboroski/Hellduck)

## License
No root license file is declared; review the repository terms before reuse.

---
**愿得一心人，白首不相离。**
*May I find one devoted heart and remain together until our hair turns white.*
— 《白头吟》
