# GUI / Visual System Standard

> Design contract for future engineering tools. Fragile-Baby is an architecture workstream/proposal; this document does not imply a verified Elbrus/E2K implementation or GUI.

## Visual identity

| Token | Value | Use |
|---|---|---|
| Primary yellow | `#FFCC00` | Main action and selected item |
| Highlight yellow | `#FFE600` | Focus and progress |
| Black / graphite | `#000000` / `#1A1A1A` | Structural surfaces and outlines |
| Error red | `#E53935` | Critical validation failures |
| Signal cyan | `#29B6F6` | Active evidence/data flow |
| White | `#FFFFFF` | Text and labels |

Existing Duck tokens/assets remain canonical where present. Migrate palette values only with all dependent code, previews and quality checks.

## Future engineering workspace

A future host tool may use a header with project mark, measured validation state and local time; a central architecture/ABI evidence canvas; a CPU/board/toolchain matrix; and contextual validation controls. The sample `55 / ~~~ / 21:33` is a wireframe placeholder, not processor telemetry.

## Architecture and target-evidence boundary

- The current repository is an architecture proposal/workstream; do not claim a supported CPU model, board, boot path, emulator or physical qualification without evidence.
- Display exact CPU model/stepping, board revision, memory map, toolchain/ABI and evidence provenance before marking a target supported.
- Separate host invariants, cross-build success, emulator results and physical hardware evidence.
- Unknown ISA/privilege/MMIO/DMA capability remains unknown and must fail closed.
- UI annotations are explanatory metadata and do not replace approved hardware documentation.

## Accessibility and release gate

Use text/icon status, keyboard focus, responsive scaling, reduced motion and WCAG AA contrast (4.5:1 normal text; 3:1 large text). Conceptual layouts are labelled **concept**. A GUI claim requires a runnable tool, tests, real screenshots and target-specific evidence independent of the GUI.

## Українська

Fragile-Baby є архітектурним напрямом/пропозицією, а не перевіреною реалізацією Elbrus/E2K чи GUI. Майбутній інструмент має показувати точну модель CPU/stepping, ревізію плати, memory map, toolchain, ABI та походження доказів. Host, cross-build, emulator і hardware validation не змішуються. `55 / ~~~ / 21:33` — умовний макет, не телеметрія процесора.

## Русский

Fragile-Baby является архитектурным направлением/предложением, а не проверенной реализацией Elbrus/E2K или GUI. Будущий инструмент должен показывать точную модель CPU/stepping, ревизию платы, memory map, toolchain, ABI и происхождение доказательств. Host, cross-build, emulator и hardware validation не смешиваются. `55 / ~~~ / 21:33` — условный макет, не телеметрия процессора.
