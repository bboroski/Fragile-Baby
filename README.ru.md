
> **Фирменная палитра:** сигнальный жёлтый `#FFD600`; глубокий чёрный `#111111`.
<h1 align="center">Fragile-Baby</h1>
<p align="center"><strong>Elbrus Architecture &amp; Platform Qualification Workstream</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-ARCHITECTURE%20PROPOSAL-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/TARGET-ELBRUS%20%2F%20E2K-FFD600?style=for-the-badge&labelColor=111111"><img src="https://img.shields.io/badge/LICENSE-NOT%20DECLARED-FFD600?style=for-the-badge&labelColor=111111"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

---

**Fragile-Baby — отдельное инженерное направление для исследования архитектуры Elbrus/E2K и подготовки проверяемой поддержки процессорной платформы.** Цель — определить точные ABI, toolchain, memory-map и boot-контракты до заявления о совместимости.

## Текущий статус

<badge>ARCHITECTURE PROPOSAL</badge>

Репозиторий содержит архитектурное предложение и справочные материалы по интеграции. Проверенной target-реализации, подтверждённого boot path или аппаратной квалификации нет. Ни одна модель процессора или плата Elbrus не объявляется поддерживаемой.

## Инженерная область

- Профили ABI и toolchain для конкретной цели.
- Проверка формата образа, memory map, диапазонов адресов и alignment.
- Проверки linker layout и секций.
- Версионируемые manifest для CPU/SoC, stepping, board revision и toolchain.
- Воспроизводимая матрица host, cross-build, emulator и physical-target evidence.
- Узкий платформенный интерфейс с явными capability gates.

## Контракт квалификации

| Уровень | Необходимые данные |
|---|---|
| CPU | Точная модель, stepping и доступные ISA/privilege features |
| Плата | Board revision, memory map, MMIO и DMA windows |
| Toolchain | Компилятор, binutils/linker, ABI и startup objects |
| Image | Формат, секции, alignment, checksum и границы адресов |
| Emulator | Конкретный эмулятор, версия и воспроизводимые результаты |
| Hardware | Физическая загрузка, serial/diagnostic output и тестовые доказательства |

Host-тесты подтверждают только программные инварианты. Они не заменяют cross-build, эмуляцию или проверку на физическом оборудовании. Свойства Elbrus нельзя выводить из ARM, x86 или RISC-V: каждый порт должен опираться на документацию конкретного CPU и платформы.

## Управление и границы

До реализации необходимо определить владельца домена, поддерживаемые варианты CPU, публичные интерфейсы, threat model, build/test strategy, лицензию и направления зависимостей. Новые интеграции должны быть версионируемыми, независимо тестируемыми и обратимыми.

Документация: [инженерная интеграция](docs/REAPER_DOMAIN_INTEGRATION.md) · [профиль границ и инвариантов](docs/CLOSED_DOMAIN_METRIC_INTEGRATION.md) · [каноническая спецификация CDM-1 в SAMBU](https://github.com/bboroski/SAMBU/blob/main/docs/CLOSED_DOMAIN_METRIC.md).

## Экосистема и лицензия

Связанные проекты: [Kloz](https://github.com/bboroski/Kloz), [ReaperCripple](https://github.com/bboroski/ReaperCripple), [NUN](https://github.com/bboroski/NUN), [NUNLauncher](https://github.com/bboroski/NUNLauncher) и [Klipot](https://github.com/bboroski/Klipot).

Файл <code>LICENSE</code> отсутствует; лицензия не объявлена. Определите условия до публичного распространения.

---

**Создано с любовью к открытой инженерии и людям.**