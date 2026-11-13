# ELBRUS E2K — Open Engineering Research & Development Initiative

**Публичная инженерная публикация · Версия 0.1.0 · 2026-11-13**  
Основной workstream: [Fragile-Baby](https://github.com/bboroski/Fragile-Baby)  
Связанный платформенный профиль: [SAMBU / platforms/e2k](https://github.com/bboroski/SAMBU/tree/main/platforms/e2k)

> Статус: исследовательская программа и инженерные предложения. Это не официальный документ МЦСТ, не заявление о сотрудничестве с МЦСТ и не подтверждение ускорения процессоров Elbrus.

## Аннотация

Публикация собирает доступные на GitHub наработки по Elbrus/E2K в проверяемую инженерную программу: платформенная идентификация, компилятор и ABI, нативное исполнение, VLIW-aware анализ, память, векторизация, профилирование, воспроизводимые сборки, межрепозиторные контракты и аппаратная квалификация.

Цель — не объявить поддержку на основании названия архитектуры, а построить цепочку доказательств. Каждое утверждение о совместимости, корректности, производительности или физическом исполнении должно иметь исходный код, конфигурацию, версию toolchain, commit SHA, журнал теста и, для аппаратных заявлений, идентификацию целевой системы.

**666 666 символов — целевой объём серии томов, а не объём уже написанной редакции.** Материал будет расширяться содержательными главами, спецификациями, тестами, приложениями и измерениями, а не механическим повторением текста.

## 1. Объём проверки GitHub

В доступном аккаунте проверены 15 публичных репозиториев: SAMBU, ToolNG, ReaperCripple, Kloz, CO, SaintSI, Klipot, NUN, NUNLauncher, Fragile-Baby, Luci, Hellduck, 9circ, BlopScore и Jungelist-Massive.

Наиболее прямые E2K-артефакты текущей выборки:

- **Fragile-Baby** — отдельный workstream исследования Elbrus/E2K и подготовки квалификации платформы. README описывает CPU/SoC identity, stepping и ABI profile, toolchain/linker/image/memory-map requirements, versioned manifest и матрицу host/cross-build/emulator/physical-target evidence. Сам README прямо сообщает, что проверенной E2K target-реализации, boot path и hardware qualification пока нет.
- **SAMBU** — каталог `platforms/e2k` с README, `target.json`, платформенной логикой и тестами. Профиль описывает 64-bit little-endian E2K Linux userspace, ELF machine `EM_MCST_ELBRUS = 175`, Linux machine name `e2k`, семейства ISA/SDK и границы native userspace, firmware и bare-metal kernel.

Для остальных репозиториев в этой выборке не найдено достаточных прямых E2K-артефактов, чтобы заявлять нативную поддержку. Их возможный вклад в экосистему должен подтверждаться конкретными файлами, коммитами, контрактами и тестами.

## 2. Что зафиксировано в SAMBU

Манифест `platforms/e2k/target.json` содержит:
- architecture: `e2k`;
- ELF class: 64 bit;
- byte order: little-endian;
- ELF machine: 175 (`EM_MCST_ELBRUS`);
- Linux machine name: `e2k`;
- execution ABI: MCST E2K Linux userspace ABI;
- compiler family: LCC;
- cross-build host: x86_64 Linux;
- перечни ISA/SDK профилей;
- physical hardware status: `not-yet-qualified`.

Это формализованный профиль, а не доказательство запуска программы на физическом процессоре.

Тесты `tests/test_platforms.py` проверяют нормализацию имён E2K, 64-битный little-endian контракт, ELF machine 175, отказ при неподходящей ширине указателя или endian, отличие x86_64 host от E2K и корректность host probe. Эти тесты полезны как host-side contract tests, но не заменяют cross-compilation, emulator execution, native execution или hardware qualification.

## 3. Границы исполнения и загрузки

Документированный для текущего профиля маршрут: firmware / PNS → Elbrus Linux → native E2K userspace process.

User-mode `qemu-e2k` для Linux-приложений не является полной эмуляцией платы, firmware или bare-metal cold boot. Успешный запуск userspace бинарного файла не доказывает работу контроллеров, периферии, interrupt routing, memory map или загрузчика.

Generic Limine нельзя автоматически объявлять E2K bootloader: загрузочный образ для другой ISA не становится E2K образом от переименования. Для отдельного bare-metal порта нужны подтверждённые boot contract, image format, entry point, memory map, interrupt model, device initialization и тесты на целевой платформе.

## 4. Исследовательские потоки

### A. Architecture and platform identity
Версионировать CPU/SoC identity, stepping, ISA profile, board revision и платформенный паспорт. Неизвестные параметры должны иметь статус unknown/not-qualified, а не заполняться предположениями.

### B. Compiler, ABI and binary pipeline
Зафиксировать LCC, assembler, linker, runtime и sysroot. Проверить ELF headers, relocations, symbol conventions, calling convention, stack alignment, register preservation и unwind behavior по первичным документам и исполняемым fixtures. Не выводить ABI из x86 или ARM.

### C. Native runtime
Разделить native Linux userspace, user-mode emulation, firmware и bare-metal kernel. Проверять startup, loader, linking, runtime libraries, memory, threads, signals, filesystem и IPC только в пределах реально доступной платформы.

### D. VLIW-aware compiler investigation
Исследовать статическое планирование LCC, зависимости операций, влияние optimization flags и качество машинного кода. Проверять branch-heavy, memory-heavy и compute-heavy kernels. Любые утверждения о ширине issue, функциональных устройствах, слотах, latency и bundle rules должны ссылаться на первичную спецификацию конкретного поколения либо на воспроизводимый эксперимент и disassembly.

### E. Memory hierarchy
Измерять latency, bandwidth, cache behavior, locality, working-set sizes, stride и alignment. Публиковать размеры данных, способ выделения памяти, число повторов, статистику разброса и условия системы.

### F. Vectorization and numerical kernels
Сравнивать scalar baseline, compiler auto-vectorization и только документированные explicit vector interfaces. Проверять точность, округление, граничные значения и воспроизводимость результата.

### G. Profiling and benchmark evidence
Каждая карточка benchmark содержит исходный код и commit, CPU/board/OS, toolchain и flags, входные данные, метод измерения, warm-up, число повторов, median, dispersion, outliers, correctness check, raw logs и digest артефакта. Недоступные hardware counters нельзя заменять вымышленными значениями.

### H. Reproducible builds and CI
Отдельные стадии: host validation → host tests → vendor cross-compile → artifact inspection → emulator smoke test (если применимо) → native E2K execution → physical qualification → performance regression. Успех одной стадии не повышает автоматически статус следующей.

### I. Cross-repository contracts
Использовать versioned schemas, stable capability IDs, explicit ABI/API versions, dependency declarations, bounded resource profiles, deterministic error codes, provenance, digests и compatibility tests. Общая тема или файл не доказывают совместимость компонентов.

### J. Security and supply chain
Фиксировать происхождение SDK/toolchain, лицензии и ограничения распространения; pin dependencies; проверять hashes; не публиковать закрытые vendor SDK, бинарники с неясными правами, секреты или ключи.

## 5. Шкала доказательств

| Статус | Смысл | Обязательное доказательство |
|---|---|---|
| proposed | Идея | Задача и критерии проверки |
| documented | Документировано | Документ и источники |
| implemented | Реализовано | Исходный код и review |
| host-tested | Проверено на host | CI log и host identity |
| cross-compiled | Собрано для E2K | Vendor toolchain, flags, artifact |
| emulator-tested | Запущено в эмуляторе | Режим эмуляции и логи |
| native-tested | Запущено нативно | E2K runtime и логи |
| hardware-qualified | Проверено на оборудовании | CPU/board identity, методика, повторяемые результаты |
| performance-validated | Производительность подтверждена | Baseline, статистика, correctness и raw measurements |

Статусы должны подтверждаться evidence records, а не маркетинговыми формулировками.

## 6. Минимальный протокол эксперимента

Каждый эксперимент публикуется с гипотезой, исходным кодом, конфигурацией target, версией ОС и toolchain, командами сборки и запуска, входными данными и seed, эталонным результатом, raw logs, статистикой повторов, ограничениями, commit SHA и SHA-256 артефактов. Компиляция, запуск, correctness и performance measurement фиксируются отдельно.

## 7. Приоритетный план

**P0 — Evidence baseline:** ревизия E2K-файлов, проверка источников и версий, единая шкала статусов, manifest schema, validator, реестр пробелов.

**P1 — Toolchain qualification:** доступный разрешённый vendor toolchain, compiler/assembler/linker/sysroot checks, ABI fixtures, cross-build CI.

**P2 — Emulator and native runner:** корректно ограниченные user-mode smoke tests, native runner на доступном E2K Linux, журналы и target identity.

**P3 — Benchmark suite:** integer, floating-point, memory, branch, vector и I/O workloads, baseline, повторяемые измерения и отчёт о разбросе.

**P4 — Optimization experiments:** один параметр на эксперимент, disassembly inspection, correctness gates, сравнение с baseline, публикация отрицательных результатов.

**P5 — Ecosystem integration:** межрепозиторные контракты, версионируемые адаптеры, integration tests, evidence catalog и воспроизводимые releases.

## 8. Что публикация не утверждает

На дату редакции не заявляется, что:
- все 15 репозиториев имеют нативную E2K поддержку;
- создан новый полноценный E2K compiler;
- реализован bare-metal kernel или bootloader;
- проведена аппаратная квалификация на Elbrus-8C/8CV/16C/32C;
- доказано ускорение реальных workloads;
- МЦСТ одобрило или поддерживает инициативу.

Модели процессоров могут быть целями исследования, но указание модели в плане не означает доступ к ней или проведённый тест.

## 9. Репозитории экосистемы

[SAMBU](https://github.com/bboroski/SAMBU) · [Fragile-Baby](https://github.com/bboroski/Fragile-Baby) · [ToolNG](https://github.com/bboroski/ToolNG) · [ReaperCripple](https://github.com/bboroski/ReaperCripple) · [Kloz](https://github.com/bboroski/Kloz) · [CO](https://github.com/bboroski/CO) · [SaintSI](https://github.com/bboroski/SaintSI) · [Klipot](https://github.com/bboroski/Klipot) · [NUN](https://github.com/bboroski/NUN) · [NUNLauncher](https://github.com/bboroski/NUNLauncher) · [Luci](https://github.com/bboroski/Luci) · [Hellduck](https://github.com/bboroski/Hellduck) · [9circ](https://github.com/bboroski/9circ) · [BlopScore](https://github.com/bboroski/BlopScore) · [Jungelist-Massive](https://github.com/bboroski/Jungelist-Massive).

Этот перечень фиксирует охват проверки, а не одинаковый вклад всех репозиториев в E2K.

## 10. Источники и ориентиры

- [SAMBU E2K platform profile](https://github.com/bboroski/SAMBU/blob/main/platforms/e2k/README.md)
- [SAMBU E2K target manifest](https://github.com/bboroski/SAMBU/blob/main/platforms/e2k/target.json)
- [SAMBU platform tests](https://github.com/bboroski/SAMBU/blob/main/tests/test_platforms.py)
- [SAMBU ecosystem execution contract](https://github.com/bboroski/SAMBU/blob/main/docs/ECOSYSTEM_EXECUTION_CONTRACT.md)
- [Fragile-Baby qualification workstream](https://github.com/bboroski/Fragile-Baby)
- [MCST developer downloads](https://dev.mcst.ru/download/)
- [MCST Elbrus SDK](https://www.mcst.ru/SDK)
- [MCST Elbrus Linux](https://www.mcst.ru/elbrus_linux)
- [MCST PNS](https://www.mcst.ru/boot)
- [MCST qemu-e2k announcement](https://www.mcst.ru/2025-12-25_qemu-e2k)
- [Limine supported architectures](https://github.com/Limine-Bootloader/Limine)

Ссылки служат ориентирами; перед каждым последующим выпуском проверяются актуальность, версии и применимость первичных документов.

## 11. План корпуса на 666 666 символов

| Том | Содержание | Плановый объём |
|---|---|---:|
| I | Архитектурная база, термины, доказательства | 55 000 |
| II | CPU/SoC identity, поколения, ISA | 65 000 |
| III | LCC, ABI, ELF, linker, binary pipeline | 75 000 |
| IV | VLIW scheduling и анализ машинного кода | 85 000 |
| V | Memory hierarchy и data movement | 65 000 |
| VI | Vectorization и numerical kernels | 65 000 |
| VII | Runtime, Linux userspace, firmware, boot | 55 000 |
| VIII | Profiling, benchmark methodology, статистика | 70 000 |
| IX | CI, reproducible builds, adapters, contracts | 55 000 |
| X | Security, supply chain, qualification, приложения | 76 666 |
| **Итого** | | **666 666** |

Это редакционный план, а не заявление о написании всех томов. Каждый выпуск должен добавлять новые данные, код, источники или тесты.

## 12. Участие и редакционная политика

Технические замечания принимаются в виде issue/PR с точным файлом, строкой, моделью CPU, версией ОС и LCC, командами, ожидаемым и фактическим результатом и логами. Приветствуются ссылки на первичные документы производителя и воспроизводимые benchmark reports.

Правила: не выдавать планы за реализацию; cross-compilation за native execution; user-mode emulation за full-system emulation; host tests за hardware qualification; неподтверждённые цифры за измерения. Публиковать ограничения, отрицательные результаты и известные дефекты. Указывать commit, версии инструментов и конфигурацию каждого результата.

## Заключение

На текущем этапе наиболее конкретные публичные E2K-артефакты — формализованный userspace profile в SAMBU и отдельный qualification workstream в Fragile-Baby. Следующий инженерный шаг — получить воспроизводимый цикл: **собрать → проверить бинарный формат → запустить → проверить корректность → измерить → сохранить доказательства → повторить**.

Открытая цель инициативы — сделать каждое предложение проверяемым, каждый результат воспроизводимым, а каждый статус подтверждаемым.

*Версия 0.1.0 подготовлена на основе доступных на 2026-11-13 файлов GitHub. Содержание уточняется по мере проверки дополнительных исходников, получения первичной документации и выполнения тестов на целевом оборудовании.*
