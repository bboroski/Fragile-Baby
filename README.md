<!-- Title: Fragile-Baby — Elbrus E2K architecture research and platform qualification -->
<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Логотип Fragile-Baby" width="76"></p>

# Fragile-Baby

> **Visual identity:** Duck Black / Yellow — accent `#FFD600`, primary ink `#111111`.

[![Documentation quality gate](https://github.com/bboroski/Fragile-Baby/actions/workflows/duck-quality-gate.yml/badge.svg?branch=main)](https://github.com/bboroski/Fragile-Baby/actions/workflows/duck-quality-gate.yml)

**Fragile-Baby** — окремий документаційно-архітектурний workstream для дослідження Elbrus/E2K та опису доказів, потрібних для перевірюваної кваліфікації цільової платформи.

<sub>Оновлено: 2026-11-11 · Стадія: architecture proposal · Target evidence: pending</sub>

> **TL;DR:** це наразі архітектурний/documentation scaffold, а не executable SDK. У репозиторії немає готової E2K реалізації, toolchain build або підтвердженого hardware boot path.

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md)

## Зміст

- [Мета workstream](#мета-workstream)
- [Поточний стан](#поточний-стан)
- [Що потрібно для кваліфікації](#що-потрібно-для-кваліфікації)
- [Як працювати з репозиторієм](#як-працювати-з-репозиторієм)
- [Межі та безпека](#межі-та-безпека)
- [Пов'язані проєкти](#повязані-проєкти)
- [FAQ](#faq)
- [Підтримка та ліцензія](#підтримка-та-ліцензія)

## Мета workstream

Fragile-Baby відокремлює дослідження архітектури Elbrus/E2K від загальних припущень про x86, Arm або RISC-V. Будь-яке твердження про сумісність має бути прив'язане до конкретного CPU/SoC, stepping, board revision, ABI та версії compiler toolchain.

## Поточний стан

На поточній гілці репозиторій містить документаційні матеріали, інженерні правила, design assets і workflow перевірки документації. **Не знайдено** E2K source implementation, CMake/Make build target, виконуваного CLI, окремого E2K toolchain або апаратних тестових доказів.

Тому тут немає команди інсталяції чи build-команди, яку можна було б чесно назвати перевіреним quick start. Робоча точка входу — [engineering governance](docs/ENGINEERING_GOVERNANCE.md) та [technical debt register](docs/TECHNICAL_DEBT_REGISTER.md).

## Що потрібно для кваліфікації

| Доказ | Що має бути зафіксовано |
|---|---|
| CPU/SoC identity | точна модель, stepping та revision |
| ABI | calling convention, data model, alignment |
| Toolchain | compiler, assembler, linker та точні версії |
| Image & memory map | формат образу, адресні межі, linker layout |
| Execution evidence | reproducible cross-build та emulator result |
| Hardware evidence | фізична плата, firmware, logs і повторюваний тест |

Значення для Elbrus/E2K не можна запозичувати з іншої ISA без окремого джерела та підтвердження.

## Як працювати з репозиторієм

1. Описуйте одне перевірюване архітектурне питання за раз.
2. Додавайте джерело специфікації, модель CPU/плати та версію toolchain.
3. Розділяйте status **proposal**, **implemented**, **host-tested**, **emulator-tested** та **hardware-qualified**.
4. Не оголошуйте target compatibility без відтворюваних доказів.

Документаційні workflow: [Duck quality gate](.github/workflows/duck-quality-gate.yml). Загальні правила: [engineering governance](docs/ENGINEERING_GOVERNANCE.md), [adaptive workspace integration](docs/ADAPTIVE_WORKSPACE_INTEGRATION.md) і [technical debt](docs/TECHNICAL_DEBT_REGISTER.md).

## Межі та безпека

Не використовуйте неперевірені регістри, адреси пам'яті, voltage/frequency values або firmware operations на фізичному обладнанні. Усі електричні й timing limits мають походити з документації конкретного виробника та підтверджуватися на цільовій платі.

## Пов'язані проєкти

- [NUN](https://github.com/bboroski/NUN) — системні boot, memory та execution contracts.
- [NUNLauncher](https://github.com/bboroski/NUNLauncher) — host-side перевірка kernel-image metadata; не є E2K bootloader.
- [ReaperCripple](https://github.com/bboroski/ReaperCripple) містить окремі embedded BSP та E2K-oriented host tests; це не доказ hardware qualification Fragile-Baby.
- [Klipot](https://github.com/bboroski/Klipot) — каталог модулів та інтеграційних контрактів.

## FAQ

**Чи підтримується Elbrus/E2K уже зараз?** Підтвердженої target-реалізації та hardware qualification у цьому репозиторії немає.

**Як зібрати проєкт?** Наразі немає build target або executable. Спершу потрібно додати перевірювану реалізацію та toolchain contract.

## Підтримка та ліцензія

Питання й пропозиції: [Issue tracker](https://github.com/bboroski/Fragile-Baby/issues) · [bug report](https://github.com/bboroski/Fragile-Baby/issues/new). Для архітектурних змін додавайте первинні джерела й evidence matrix. Профіль супроводу: [bboroski](https://github.com/bboroski).

**Ліцензія не оголошена:** файл LICENSE відсутній. Не припускайте дозволу на копіювання або комерційне використання.
