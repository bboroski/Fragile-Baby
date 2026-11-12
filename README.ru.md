# Fragile-Baby
**Elbrus Architecture & Platform Qualification**

[Українська](README.md) · [English](README.en.md) · [Русский](README.ru.md)

Инженерное направление исследования Elbrus/E2K и подготовки проверяемой квалификации платформы.

## Возможности
- Профили идентичности CPU/SoC, stepping и ABI.
- Требования к toolchain, linker layout, image format и memory map.
- Версионированные manifest для CPU, ревизии платы и compiler toolchain.
- Матрица доказательств host, cross-build, emulator и physical target.

## Запуск и проверка
```bash
python3 tools/evidence_advisor.py
```

## Границы
Проверенная E2K target-реализация, boot path или hardware qualification отсутствуют. Host-тесты не доказывают совместимость с Elbrus; параметры нельзя выводить из другой ISA.

## Документация проекта
Проект посвящён спецификациям и матрицам доказательств, а не GUI. Фальшивые снимки оборудования не используются.

## Связанные проекты
[Evidence advisor](docs/EVIDENCE_ADVISOR.md) · [NUN](https://github.com/bboroski/NUN) · [Hellduck](https://github.com/bboroski/Hellduck)

## Лицензия
Корневой LICENSE не объявлен; перед повторным использованием проверьте условия репозитория.

---
**愿得一心人，白首不相离。**
*Найти человека с верным сердцем и оставаться вместе до седых волос.*
— 《白头吟》
