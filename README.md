<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Duck mark" width="104"></p>

<h1 align="center">Fragile-Baby</h1>
<p align="center"><strong>Elbrus Architecture &amp; Platform Qualification Workstream</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-ARCHITECTURE%20PROPOSAL-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/TARGET-ELBRUS%20%2F%20E2K-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/LICENSE-NOT%20DECLARED-FFD600?style=for-the-badge&labelColor=111111"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>


<p align="center"><sub><a href="design/DUCK_UI_SYSTEM.md">Duck Black / Yellow UI standard</a> · <a href="assets/duck-ui/duck-ui-preview.svg">Vector UI preview</a></sub></p>

**Fragile-Baby — окремий інженерний напрям для дослідження архітектури Elbrus/E2K та підготовки перевірюваної підтримки процесорної платформи.** Завдання проєкту — визначити точні ABI, toolchain, memory-map і boot-контракти до заяви про сумісність.

## Поточний стан

<badge>ARCHITECTURE PROPOSAL</badge>

Репозиторій наразі містить архітектурну пропозицію та інтеграційні довідкові матеріали. Перевіреної target-реалізації, підтвердженого boot path або апаратної кваліфікації немає. Жодна модель процесора чи плата Elbrus не оголошується підтримуваною.

## Інженерний обсяг

- Target-specific ABI та toolchain profiles.
- Перевірка формату образу, memory map, address ranges та alignment.
- Перевірки linker layout і секцій.
- Версійований manifest CPU/SoC, stepping, board revision та інструментального ланцюга.
- Відтворювана матриця host, cross-build, emulator і physical-target evidence.
- Вузький платформний інтерфейс із явними capability gates.

## Контракт кваліфікації

| Рівень | Що потрібно зафіксувати |
|---|---|
| CPU | Точна модель, stepping та доступні ISA/privilege features |
| Плата | Board revision, memory map, MMIO і DMA windows |
| Toolchain | Компілятор, binutils/linker, ABI та startup objects |
| Image | Формат, секції, alignment, checksum і межі адрес |
| Emulator | Конкретний емулятор, версія та відтворювані результати |
| Hardware | Фізичний запуск, serial/diagnostic output і тестові докази |

Host-тести підтверджують лише програмні інваріанти. Вони не замінюють cross-build, емуляцію або перевірку на реальному обладнанні. Параметри Elbrus не можна виводити з ARM, x86 чи RISC-V: кожен порт має спиратися на документацію конкретного CPU та платформи.

## Межі та управління

До реалізації потрібно зафіксувати власника домену, підтримувані варіанти CPU, публічні інтерфейси, threat model, build/test strategy, ліцензію й напрямки залежностей. Нові інтеграції мають бути версійованими, незалежно тестованими та зворотними.

Документація: [інженерна інтеграція](docs/REAPER_DOMAIN_INTEGRATION.md) · [профіль меж і інваріантів](docs/CLOSED_DOMAIN_METRIC_INTEGRATION.md) · [канонічна специфікація CDM-1 у SAMBU](https://github.com/bboroski/SAMBU/blob/main/docs/CLOSED_DOMAIN_METRIC.md).

## Екосистема та ліцензія

Пов'язані проєкти: [Kloz](https://github.com/bboroski/Kloz), [ReaperCripple](https://github.com/bboroski/ReaperCripple), [NUN](https://github.com/bboroski/NUN), [NUNLauncher](https://github.com/bboroski/NUNLauncher) та [Klipot](https://github.com/bboroski/Klipot).

Файл <code>LICENSE</code> відсутній; ліцензію не оголошено. Умови використання потрібно визначити до публічного розповсюдження.

---

**Створено з любов'ю до відкритої інженерії та людей.**

## E2K / Elbrus support

This repository now contains the E2K target profile and shared LCC toolchain. Current maturity is architecture profile and integration planning only; it does not yet provide a bootloader, firmware interface, kernel or native runtime. See [the E2K workstream](docs/E2K_ELBRUS.md).
