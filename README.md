# Fragile-Baby

**Status:** project placeholder and integration-reference scaffold.

The repository currently contains no product implementation, public API, build system, supported hardware target, or test suite. Its intended product role still needs to be defined; this README deliberately does not invent one.

## Cross-project domain references

- [Reaper-inspired engineering integration notes](docs/REAPER_DOMAIN_INTEGRATION.md)
- [Canonical 50-pattern engineering catalogue in SAMBU](https://github.com/bboroski/SAMBU/blob/main/data/reaper/engineering_patterns_50.tsv)
- [Academic biology glossary in SAMBU](https://github.com/bboroski/SAMBU/blob/main/data/biology/academic_terms_500.tsv)

These references are passive documentation and research vocabulary only. They do not imply that Fragile-Baby implements a runtime, biological model, AI system, hardware controller, or Mass Effect technology.

## Promotion gate

Before implementation, define the repository owner role, supported platforms, public interfaces, threat model, build/test strategy, licensing requirements, and dependency direction. Only then should executable code or ecosystem capabilities be introduced. Any future integration must be versioned, independently testable, and reversible.



**Призначення:** відтворювана перевірка компіляторів, ABI, toolchain та платформних адаптерів для процесорної архітектури Elbrus / E2K.

[English](README.en.md) · [Русский](README.ru.md)

## Поточний стан

Це початковий інженерний каркас: JSON-профіль E2K, його валідатор і тести. Репозиторій **ще не заявляє повної підтримки процесорів Elbrus**. Тут поки немає перевіреного vendor toolchain, BSP, драйверів, linker scripts, завантажуваного runtime або результатів тестування на фізичному обладнанні.

## Напрямки роботи

- точна ідентифікація моделі процесора, плати та ревізії;
- відтворювані toolchain-профілі з compiler version, target triple, sysroot, linker і ABI;
- переносні C11-контракти з Kloz, CO та SaintSI;
- qualification-адаптери ReaperCripple лише після перевірки реального toolchain;
- узгоджені boot та capability-контракти з NUN і NUNLauncher;
- host-тести окремо від emulator- і hardware-тестів.

## Перевірка профілю

Потрібен Python 3.10+ без сторонніх пакетів.

```sh
python3 tools/validate_toolchain_profile.py profiles/elbrus.template.json
python3 -m unittest discover -s tests -v
```

Шаблон навмисно містить значення unknown і має статус unverified. Це не робоча конфігурація компілятора.

## Правило доказів

Статус target-validated дозволений лише коли зафіксовані конкретна модель і ревізія плати, точні версії compiler/linker/sysroot, команда збірки, артефакт, результати перевірок і посилання на відтворювані журнали. Рекомендація Gemini чи іншої моделі не є доказом сумісності.

Див. [Elbrus qualification plan](docs/ELBRUS_QUALIFICATION.md) та [профіль toolchain](profiles/elbrus.template.json).

## Межі безпеки

Профілі не виконують команди, не змінюють частоти, напруги, регістри або boot-конфігурацію. Жоден параметр не можна переносити з іншої моделі CPU без окремого підтвердження. Не використовувати цей каркас для прошивання фізичного обладнання.
