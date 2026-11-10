<p align="center"><strong>FRAGILE-BABY</strong></p>
<p align="center"><strong>Elbrus Platform Support Workstream</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-ARCHITECTURE%20PROPOSAL-FFD600?style=for-the-badge&labelColor=111111" /> <img src="https://img.shields.io/badge/FOCUS-ELBRUS%20QUALIFICATION-FFD600?style=for-the-badge&labelColor=111111" /></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

# Fragile-Baby

**Робочий напрям для системної перевірки підтримки процесорів Elbrus — від точного ABI та toolchain до верифікації образу й цільової платформи.**

> **Поточний статус:** архітектурна пропозиція та інтеграційний каркас. Перевіреної реалізації, boot path або кваліфікованої плати наразі не заявлено.

## Продуктова роль

Fragile-Baby має забезпечити відтворюваний спосіб оцінити, чи може конкретна конфігурація CPU/SoC, ABI, компілятора, linker і плати підтримати заданий системний сценарій. Жодна властивість не переноситься автоматично з Arm, x86, RISC-V або іншої родини процесорів.

## Напрями функціонального розвитку

- **Профілі цілі:** точна модель CPU/SoC, ревізія, ISA-профіль, ABI та плата.
- **Toolchain matrix:** компілятор, assembler, linker, runtime, startup objects і версії.
- **Image validation:** формат, межі, вирівнювання, переповнення адресної арифметики та контроль цілісності.
- **Linker audit:** секції, entry point, memory regions, stack, reserved ranges та map-файл.
- **Evidence pipeline:** окремі результати host-check, cross-build, emulator run і фізичної перевірки.
- **Compatibility ledger:** версії інтерфейсів, відомі обмеження, regressions і правила міграції.

Це план розвитку, а не перелік уже реалізованих можливостей.

## Початок роботи

Репозиторій наразі документаційний. Ознайомтеся з:
- [Closed-domain integration profile](docs/CLOSED_DOMAIN_METRIC_INTEGRATION.md)
- [Product system and feature governance](docs/PRODUCT_SYSTEM.md)

Автоматична перевірка документації:

```bash
python .github/scripts/duck_quality_gate.py
```

## Критерії підтвердження підтримки

| Етап | Обов'язковий доказ |
|---|---|
| Target definition | Точний CPU/SoC, stepping, плата та ISA |
| ABI/toolchain | Версії компілятора, linker, ABI та startup files |
| Cross-build | Відтворювана збірка й збережені build logs |
| Image/linker | Валідований образ, map-файл, межі та entry point |
| Emulator | Відтворюваний запуск і журнал тестів, якщо доступний |
| Hardware | Результат на конкретній фізичній платі |

Поки ці докази відсутні, статус залишається **NOT VERIFIED**. Host-тест не є доказом роботи на Elbrus.

## Безпека та управління

Не вгадувати memory map, privilege mode, cache/DMA правила або розширення ISA. Помилка чи відсутність toolchain мають бути видимими станами, а не прихованим fallback. Кожен новий capability отримує ID, критерії приймання, тести, власника ролі та план відкату.

## Дизайн і комунікація

Візуальна основа екосистеми: чорне полотно `#111111`, жовтий акцент `#FFD600`, чітка типографіка, контрастні стани й доступна навігація. Маркетинг відділяє пропозиції від реалізованих і перевірених результатів.

**Fragile-Baby — з турботою про точність кожного системного контракту.**
