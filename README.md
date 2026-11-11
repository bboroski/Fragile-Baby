# Fragile-Baby
**Дослідження Elbrus/E2K та кваліфікація платформних доказів.**

Формалізує вимоги до CPU, ABI, toolchain і hardware evidence для перевірюваного платформного порту.

## Можливості
- CPU/SoC, stepping та ABI identity profile.
- Toolchain, linker layout, image format і memory-map requirements.
- Versioned manifest для CPU, board revision і compiler toolchain.
- Матриця host, cross-build, emulator та physical-target evidence.
- Capability gates і явні межі платформного порту.

## Запуск і перевірка
```bash
python3 tools/evidence_advisor.py
```

## Додатково
Команда аналізує E2K evidence matrix і показує покриття та наступну стадію. Деталі: [E2K Evidence Advisor](docs/EVIDENCE_ADVISOR.md).

Проєкт зосереджений на матрицях доказів і платформних специфікаціях, а не на GUI. Не використовуються вигадані скриншоти обладнання.

## Межі
Підтвердженої E2K target-реалізації, boot path або hardware qualification немає. Host-тести не доводять сумісність з Elbrus; параметри не виводяться з інших ISA.

## Пов'язані проєкти
[NUN](https://github.com/bboroski/NUN) · [Hellduck](https://github.com/bboroski/Hellduck)

## Ліцензія
Ліцензію не оголошено.

---
**「愿得一心人，白首不相离。」**
*«Знайти єдине серце й залишатися разом до сивини».*
— «Біла голова» (《白头吟》), давня юефуська поезія