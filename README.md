<p align="center"><img src="assets/duck-ui/duck-mark.svg" alt="Fragile-Baby mark" width="92"></p>
<h1 align="center">Fragile-Baby</h1>
<p align="center"><strong>Elbrus Architecture & Platform Qualification Workstream</strong></p>
<p align="center"><img src="https://img.shields.io/badge/STATUS-ARCHITECTURE%20PROPOSAL%20%C2%B7%20TARGET%20EVIDENCE%20PENDING-FFD600?style=for-the-badge&labelColor=111111" alt="Architecture proposal · target evidence pending"></p>
<p align="center"><a href="README.md">🇺🇦 Українська</a> · <a href="README.en.md">🇬🇧 English</a> · <a href="README.ru.md">🇷🇺 Русский</a></p>

> **Fragile-Baby** — Fragile-Baby — окремий інженерний напрям для дослідження Elbrus/E2K та підготовки перевірюваної кваліфікації платформи.

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

## NUN Mesh та пов'язані репозиторії
[SAMBU](https://github.com/bboroski/SAMBU) · [ToolNG](https://github.com/bboroski/ToolNG) · [ReaperCripple](https://github.com/bboroski/ReaperCripple) · [Kloz](https://github.com/bboroski/Kloz) · [CO](https://github.com/bboroski/CO) · [SaintSI](https://github.com/bboroski/SaintSI) · [Klipot](https://github.com/bboroski/Klipot) · [NUN](https://github.com/bboroski/NUN) · [NUNLauncher](https://github.com/bboroski/NUNLauncher) · [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) · [Luci](https://github.com/bboroski/Luci)

Репозиторії зберігають власні назви, код, API, цикли випуску та межі відповідальності. Інтеграція означає узгоджені контракти, а не автоматичне злиття незалежних runtime.

## Дизайн і документація
Базовий інтерфейсний напрям екосистеми — **Duck Black / Yellow**: чорні поверхні, жовтий акцент для дій і станів, читабельна типографіка, доступний контраст, клавіатурна навігація та підтримка reduced motion. Деталі дивіться в [design/DUCK_UI_SYSTEM.md](design/DUCK_UI_SYSTEM.md), якщо файл присутній у цьому репозиторії.

## Ліцензія
Ліцензію не оголошено; файл LICENSE відсутній.

---
**Створено з любов'ю до інженерії, системності та людей.**

## Федерація Hellduck

Цей репозиторій входить до федерації [Hellduck](https://github.com/bboroski/Hellduck) — спільного каталогу проєктів, контрактних зв’язків і станів інтеграції. Вихідний код, API, тести та цикл випуску залишаються відповідальністю цього репозиторію; Hellduck індексує зв’язки й не завантажує та не виконує код учасників. Практичні сценарії взаємодії, типи адаптерів і межі сумісності: [Integration Playbook](https://github.com/bboroski/Hellduck/blob/main/docs/INTEGRATION_PLAYBOOK.md).


## UTYA-ZHNETS machine design

This project includes an original industrial machine-design profile and machine-readable tokens. The profile extends the existing brand and does not claim unimplemented runtime features: [design profile](design/UTYA_ZHNETS.md) · [tokens](design/utya-zhnetz.tokens.json).
