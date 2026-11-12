<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Fragile-Baby mark" width="92"></p>
<h1 align="center">Fragile-Baby</h1>
<p align="center"><strong>Elbrus Architecture & Platform Qualification Workstream</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-ARCHITECTURE%20PROPOSAL%20%C2%B7%20TARGET%20EVIDENCE%20PENDING-FFD600?style=for-the-badge&labelColor=111111" alt="Architecture proposal · target evidence pending"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

> **Fragile-Baby** — Fragile-Baby — окремий інженерний напрям для дослідження Elbrus/E2K та підготовки перевірюваної кваліфікації платформи.

<sub>Оновлено: 2026-11-12</sub>

## Поточні можливості
- CPU/SoC, stepping та ABI identity profile.
- Toolchain, linker layout, image format і memory-map requirements.
- Versioned manifest для CPU, board revision і compiler toolchain.
- Host, cross-build, emulator та physical-target evidence matrix.
- Явні capability gates і межі платформного порту.

## Швидкий старт і перевірка
```bash
Перевірте специфікації й qualification documents; target build вимагає конкретного toolchain та обладнання.
```

## Архітектура, межі та достовірність
Перевіреної E2K target-реалізації, boot path або hardware qualification наразі немає. Host-тести не доводять сумісність Elbrus; параметри не виводяться з інших ISA.

## Аналіз доказів кваліфікації

`python3 tools/evidence_advisor.py` перевіряє матрицю E2K, показує послідовне покриття та наступну стадію без підміни host-перевірок апаратною кваліфікацією. Документація: [E2K evidence advisor](docs/EVIDENCE_ADVISOR.md).

## Інженерна якість
- Перевіряйте збірку й тести саме для цільової платформи; host CI не замінює hardware qualification.
- Статуси **implemented**, **partial**, **planned** мають підтверджуватися кодом, тестами та документацією.
- Не оголошуйте функцію production-ready лише на підставі макета, специфікації чи відкритого Pull Request.
- Зовнішні інтеграції мають бути явними, версіонованими, ізольованими й перевірюваними.

## Ліцензія
Ліцензію не оголошено; файл LICENSE відсутній.

---

## Статус інтеграцій

- Репозиторій зберігає власні API, збірку, тести та цикл випуску; міжпроєктна взаємодія відбувається через явні версіоновані контракти.
- STaas (SaaS integration control plane) і MoonTreach (CI/test acceleration) розвиваються окремими Pull Requests. Їх не слід вважати можливостями `main` або production-ready до злиття та проходження обов'язкових перевірок.
- Правила федерації та інтеграції: [Hellduck Integration Playbook](https://github.com/bboroski/Hellduck/blob/main/docs/INTEGRATION_PLAYBOOK.md).

## Інженерний стандарт
Індекс аудиту, тестових воріт, безпеки, супроводу та критеріїв інтеграції: [Engineering Improvement Index](docs/ENGINEERING_IMPROVEMENT_INDEX.md).

## Інтеграційні межі
Зберігайте незалежні API, runtime та цикли випуску; інтегруйте через версіоновані контракти. [Hellduck Integration Playbook](https://github.com/bboroski/Hellduck/blob/main/docs/INTEGRATION_PLAYBOOK.md).

---
**「在天愿作比翼鸟，在地愿为连理枝。」**

*«У небі — птахами-нерозлучниками, на землі — гілками одного дерева».*
