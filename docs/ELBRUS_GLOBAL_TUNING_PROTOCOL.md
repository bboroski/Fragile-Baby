# Глобальный протокол инженерной оптимизации Elbrus / E2K

**Версия:** 2.0.0  
**Канонический владелец квалификации:** Fragile-Baby  
**Область:** E2K Linux userspace, MCST LCC, машинный код, измерения производительности и NUN Mesh  
**Статус:** инженерный стандарт, не сертификат аппаратной поддержки

> Цель — получить максимально быстрый, корректный, воспроизводимый код на конкретной модели Эльбруса. Оптимизация является улучшением только при сохранении корректности и доказанном выигрыше на указанном целевом оборудовании.

## 0. Основные инварианты

1. **Сначала установить точную конфигурацию:** CPU/SoC, stepping, плата, PNS/firmware, ОС и ядро, ABI, ISA-вариант, LCC, SDK/sysroot и библиотеки.
2. **Не выводить поддержку из названия архитектуры.** E2K, e2k-v5/v6/v7, vendor SDK target и возможности QEMU — разные поля. Модельный таргет выбирается по документации установленного SDK.
3. **Разделять доказательства:** host, cross-build, QEMU user-mode, native E2K runner и физический стенд — отдельные ступени.
4. **Оптимизировать измеряемую нагрузку.** Заполненность широкого командного слова — диагностический сигнал, а не самостоятельная цель.
5. **Не применять недокументированные регистровые, MMIO, частотные, напряженческие или firmware-настройки.** Изменения железа возможны только через документированный интерфейс конкретной платы и с разрешением оператора.
6. **Сохранять переносимый путь.** Общий C11/C++ код не зависит от E2K intrinsics; ISA-специфика изолируется в адаптерах с проверяемым fallback.
7. **Каждая настройка имеет владельца, версию, доказательство и откат.** Экспериментальные флаги не попадают в production без тестов и целевых бенчмарков.

## 1. Исправление универсальных директив исходного протокола

| Исходное утверждение | Инженерная редакция |
|---|---|
| Каждый ШК обязан быть заполнен на 100%, nop запрещены | Компоновка ШК зависит от зависимостей, задержек, исполнительных устройств, ABI и версии компилятора. Анализировать горячие циклы; не запрещать корректные задержки механически. |
| Любая операция должна быть спекулятивной/предикатной | Расписание и предикатное выполнение прежде всего оставлять компилятору. Ручные преобразования допустимы после доказательства эквивалентности и проверки исключений. |
| Все циклы полностью разворачивать | Развёртка может увеличить размер кода, давление на регистры и cache footprint. Проверять локально по latency, throughput и code size. |
| Всегда применять -O4 и -funroll-loops | LCC -O0…-O4 документированы, но -O4 экспериментален и может ухудшить результат. Проверять каждый флаг на установленной версии LCC; не переносить GCC-флаги без проверки. |
| Принудительно назначать регистры через неподтверждённые атрибуты | Регистровые окна, глобальные регистры и calling convention — ответственность компилятора и ABI. Не применять неподтверждённые атрибуты. |
| Все структуры выравнивать на 128 байт | Выравнивание выводится из ABI, операции, типа, ширины вектора и измеренной геометрии cache. Размер cache line не универсален. |
| Использовать __builtin_mcc_pref() и stnt повсеместно | Intrinsics и мнемоники применять только если они подтверждены заголовками и руководством конкретного SDK. |
| SIMD-регистры всегда 64-байтные | Ширина зависит от поколения/модели. В материалах МЦСТ для 8СВ указан SIMD-128 (128 бит), а не 64 байта. Для 128 бит — до 2 double или 4 float. |
| FMA всегда выполняется за один такт и даёт 2× | FMA не гарантирует latency, throughput или удвоение. Проверять сгенерированный код, численную точность и реальный benchmark. |
| На всех моделях известны MESI/NUMA-домены | Не предполагать протокол когерентности, cache topology или NUMA без документации CPU/платы и topology ОС. |
| cpupower performance гарантирует максимальную частоту | Governor, частоты, thermal/power limits зависят от платы, firmware и ядра. Не форсировать универсальной командой. |
| isolcpus даёт нулевые context switch | Affinity, cpuset, IRQ affinity и nohz_full могут уменьшить interference, но не дают нулевых переключений или прерываний. |
| Статическая линковка всегда быстрее и безопаснее | -static — режим упаковки. Он не гарантирует меньшую задержку или лучшую безопасность; учитывать NSS, sysroot, лицензии и обновление уязвимостей. |
| Bare metal/Tiny OS — универсальный путь | Подтверждённый маршрут NUN E2K сейчас: MCST PNS → Elbrus Linux → native E2K userspace process. Bare-metal kernel требует отдельного boot ABI, exception, interrupt, memory-map и device-init пути. |
| Fixed-point всегда быстрее FP | Fixed-point допустим только при определённых диапазонах, overflow и численной погрешности. Сравнивать с FP/vector kernels. |
| PMU всегда предоставляет IPC/cache/branch counters | События зависят от CPU, ядра, драйвера и прав. Подтверждать каждое событие, отсутствующее отмечать unavailable, не нулём. |

## 2. Матрица компилятора MCST LCC

LCC — фирменный оптимизирующий компилятор МЦСТ для C/C++/Fortran. SDK включает compiler, assembler/disassembler/linker, debugger, profiling и code-coverage инструменты. Cross-LCC может работать на x86-64 и выдавать E2K-артефакт; доступ к SDK регулируется поставщиком.

### 2.1. Профили

| Профиль | Параметры | Назначение |
|---|---|---|
| debug | -O0 -g | Отладка и соответствие исходному коду |
| conservative | -O2 | Умеренно оптимизированный контрольный вариант |
| baseline | -O3 | Основная точка сравнения |
| aggressive | -O4 | Эксперимент; сравнить корректность, код и benchmark против -O3 |
| pgo-generate | -O3 -fprofile-generate | Первый проход на репрезентативном workload |
| pgo-use | -O3 + совместимый профиль | Второй проход; фиксировать происхождение профиля |

### 2.2. Опции, требующие локального подтверждения

Руководство МЦСТ описывает следующие опции; их применимость проверяется для каждой версии LCC, ISA и нагрузки:

- -fprefetch — разрешает предподкачку в циклах; тестировать на регулярном доступе.
- -fcache-opt — оптимизации совмещения блокировок в конвейеризированных циклах.
- -fno-apb — отключение APB для контрольного эксперимента.
- -faligned — разрешает предполагать выравнивание; включать только при доказанном инварианте.
- -faligned-check — диагностический контроль невыровненных обращений; fault может завершиться SIGBUS.
- -ffast — режим с изменениями оптимизационных предположений и численной семантики; не использовать в чувствительных участках без оценки ошибки. Руководство связывает его также с предположениями о выравнивании.

Принятие флага компилятором не доказывает ускорение, корректность на всех входах или физическую совместимость.

### 2.3. Обязательный цикл

1. Зафиксировать commit, compiler/version, SDK/sysroot и параметры.
2. Собрать -O2 и -O3; выполнить полный набор тестов.
3. Для горячих участков сохранить -S и, при необходимости, -fverbose-asm; изучить листинг штатными средствами MCST (ldis/debugger/profiler) или совместимыми binutils.
4. Затем проверять один фактор: -O4, PGO, prefetch/cache options, inlining, layout или vectorization.
5. Повторить тесты корректности и benchmark; сравнить медиану нескольких прогонов и размер бинарника.
6. Сохранить отчёт и артефакт; откатить вариант без воспроизводимого выигрыша.

## 3. Аппаратная и программная настройка

### 3.1. VLIW и машинный код
- Использовать листинг lcc -S и подробную разметку ассемблера там, где доступна.
- Анализировать расписание горячих циклов: зависимости, latency загрузок, переходы/вызовы, преобразования и spill/reload.
- Не измерять «процент заполнения ШК» без методики, области и состава операций.
- Ручной assembly допустим только с тестами эквивалентности, исключений и benchmark; сохранять portable fallback.

### 3.2. Регистры и calling convention
- Соблюдать ABI и распределение регистров LCC.
- Снижать spill pressure через уменьшение live ranges, лишнего состояния и локальное изменение inlining.
- always_inline/noinline — локальные эксперименты; обе крайности могут ухудшить результат.
- Размер окна и служебные поля ШК анализировать по листингу, но не менять неподдержанными атрибутами.

### 3.3. Память и кэш
- Измерять последовательный/случайный доступ, stride, working set и конкуренцию потоков.
- Проверять AoS/SoA, плотность данных, layout и повторное использование.
- Выравнивать только при доказанной необходимости и проверке реального адреса.
- Prefetch/APB проверять для конкретных шаблонов; учитывать cache pollution и лишние загрузки.
- Non-temporal операции применять только при подтверждённой ISA и измеримом выигрыше.

### 3.4. Векторизация и математика
- Разделять scalar и vector kernels; использовать документированные types/intrinsics или auto-vectorization LCC.
- Проверять ширину регистра и lane count на целевом ISA-профиле.
- Тестировать rounding, FMA contraction, NaN/Inf, signed zero и overflow.
- Сравнивать vendor EML/BLAS/LAPACK с portable kernels при наличии и разрешённой поставке.
- Fixed-point и приближённые функции требуют явного бюджета ошибки.

### 3.5. Потоки и ОС
- Определять число ядер и topology документированными интерфейсами.
- Измерять масштабирование 1/2/N потоков, false sharing, migration, contention и memory bandwidth.
- Affinity/cpuset/IRQ affinity/real-time scheduling — отдельный системный профиль с правами администратора и журналом исходного состояния.
- Не менять governor, частоту, voltage, firmware или kernel cmdline без board-specific документации и rollback.

## 4. Интеграция всех репозиториев GitHub

Репозитории остаются самостоятельными; обмен выполняется через версионированные manifests, fixtures, артефакты и API.

| Репозиторий | Вклад в общий E2K стек | Граница ответственности |
|---|---|---|
| Fragile-Baby | CPU/stepping/board/toolchain identity, tuning profiles, evidence advisor, qualification gates, benchmark evidence | Host/cross evidence не становится аппаратной квалификацией |
| NUN | Native E2K Linux runtime, C11 system contracts, сборка и self-hosted execution | Текущий профиль userspace, не bare-metal kernel |
| NUNLauncher | ELF64/LE, EM_MCST_ELBRUS=175, manifest, размер и SHA-256 admission | Проверка файла не запускает его и не аутентифицирует издателя без подписи |
| ReaperCripple | Переносимые embedded/runtime компоненты и E2K platform adapter | Host test не заменяет E2K runner/плату |
| SAMBU | Typed HIR/MIR/LIR, будущий E2K backend, scientific workloads | Native slice — ранний compiler kernel, не полный source-to-machine-code |
| Kloz | Arena, resource budgets, memory policy | Архитектурно-нейтральная основа; CPU-specific policy через adapter |
| CO | Детерминированный lifecycle компонентов | Состояния без привилегированных side effects |
| SaintSI | CRC, health signals, telemetry contracts | Телеметрия сама по себе не доказывает корректность измерителя |
| ToolNG | Read-only device evidence и диагностика | Windows host utility; не объявлять E2K hardware probe |
| Luci | Домены, реестры, policy/evidence validation | Control plane не является E2K runtime/loader |
| Klipot | Интеграционный портал, manifests и contract checks | Не исполняет код из соседних репозиториев |
| Hellduck | Федерация workspace, source contracts, integration status | Не заменяет истории и releases исходных репозиториев |
| Jungelist Massive | Исследование языков, IR и генераторов | E2K backend — отдельный проверяемый codegen target |
| BlopScore | Модель observability и аппаратной аналитики | Текущий brief ориентирован на Windows 11; E2K порт отдельный |
| 9circ | Интеграция только после подтверждения назначения и тестов | Не приписывать неподтверждённую E2K-функцию |

### Межрепозиторный контракт

Каждый E2K-зависимый компонент публикует:
- schema_version, architecture, cpu_model, stepping, board_revision;
- os, kernel, abi, isa_profile;
- compiler_family, compiler_version, compiler_binary_digest, sysroot_id;
- build_profile, все compile/link flags, static/dynamic policy;
- artifact_sha256, ELF class, endianness, machine id;
- stage: host, cross-build, emulator, native-runner или physical-target;
- test results, benchmark methodology, workload digest, logs и CI run URL;
- limitations, reviewer и дату доказательства.

Неизвестное записывается как unknown/null. Запрещено подставлять CPU, ISA, cache line, FMA units или доступность PMU по аналогии с другой моделью.

## 5. Qualification pipeline

| Стадия | Минимальный результат | Не доказывает |
|---|---|---|
| Host | Python/C11 contract tests, schema, parsers | E2K ABI и выполнение машинного кода |
| Cross-build | LCC создаёт ELF64 little-endian E2K; зафиксированы toolchain/sysroot/digest | Выполнение бинарника |
| Emulator | Запуск в документированном QEMU user profile | Физическую плату, firmware, периферию и непокрытые ISA |
| Native E2K runner | Запуск на runner с uname e2k, CPU/compiler identity и CI logs | Поддержку любых других CPU/stepping |
| Physical target | Идентифицированный CPU/плата, повторяемые прогоны, журнал среды и независимая проверка | Конфигурации вне указанной матрицы |

uname -m=e2k сам по себе не завершает физическую квалификацию. Hardware-qualified присваивается только после проверки полной матрицы независимым reviewer.

## 6. Benchmark стандарт

1. Сохранить baseline и фиксированный набор входных данных.
2. Проверять результат/checksum до измерения времени.
3. Прогреть workload; провести не менее 7 измеряемых повторов, когда нагрузка это допускает; записать median, разброс и outliers.
4. Сравнивать одинаковые CPU/stepping, ОС/ядро, compiler build, power/thermal conditions и input digest.
5. Публиковать throughput, latency (p50/p95 для системных задач), code size, память, число потоков и флаги.
6. Менять один существенный фактор за раз; комбинации подтверждать отдельным экспериментом.
7. Не публиковать «ускорение в X раз» без baseline, методики, raw data и commit.
8. Для FP публиковать максимальную/среднюю ошибку и режим округления.
9. Для streaming kernels измерять working set, stride, alignment и число потоков.
10. Не сравнивать host emulation и физический target как эквивалентные стенды.

## 7. CI и release gates

- PR/host CI: tooling syntax, unit tests, JSON Schema, evidence advisor, repository contracts.
- Cross-build: лицензированный cross-LCC runner, compiler version и sysroot.
- Emulator: только ISA/profile, заявленные конкретной версией QEMU user emulator.
- Native: self-hosted runner labels linux,e2k; read-only checks, build, tests, benchmark, logs.
- Physical qualification: ручное утверждение, идентифицированная плата, журнал, raw results, reviewer.
- Release: SBOM, SHA-256, provenance и ссылки на qualification evidence. Host-only release не получает hardware-qualified.

## 8. Аппаратная безопасность и откат

Запрещено автоматически:
- менять напряжение, частоты, power limits, PNS/firmware, bootloader, kernel cmdline, kernel modules или регистры периферии;
- отключать thermal/power safeguards, cache/MMU protection;
- прошивать плату, перезаписывать диски или запускать неизвестный образ;
- подменять x86 image на E2K artifact;
- считать эмуляцию физической квалификацией.

Любая системная настройка требует исходного значения, документа производителя, operator approval, stop criteria, журнала, rollback и проверки после отката.

## 9. Поэтапная реализация

- **P0 — Identity & evidence:** единый manifest/schema для Fragile-Baby, NUN, NUNLauncher и ReaperCripple.
- **P1 — Toolchain audit:** LCC/SDK/sysroot, flags, ELF header, artifact digest.
- **P2 — Benchmark base:** portable C11 microbenchmarks, correctness и повторяемые измерения на E2K runner.
- **P3 — Optimization experiments:** -O2/-O3/-O4, PGO, inlining, prefetch/cache, alignment, vector kernels по одному фактору.
- **P4 — Compiler/backend:** SAMBU typed IR → target capability model → E2K lowering → object/link → ELF/native proof.
- **P5 — System integration:** NUN userspace/runtime, ReaperCripple adapter, Kloz/CO resource/lifecycle contracts и NUNLauncher admission.
- **P6 — Independent qualification:** CPU/stepping/board matrix, thermal stability, regression suite, throughput/latency и reviewer sign-off.

## 10. Официальные источники

- [Руководство по эффективному программированию на платформе «Эльбрус» 1.2](https://dev.mcst.ru/book/index.html)
- [Опции компилятора LCC](https://dev.mcst.ru/book/chapter1.html)
- [Макросы __e2k__ и __LCC__](https://dev.mcst.ru/book/chapter2.html)
- [Архитектура и регистровая организация](https://dev.mcst.ru/book/chapter4.html)
- [Анализ производительности и машинного кода](https://dev.mcst.ru/book/chapter5.html)
- [Повышение производительности и PGO](https://dev.mcst.ru/book/chapter6.html)
- [Система программирования «Эльбрус» (SDK)](https://www.mcst.ru/SDK)
- [Компилятор LCC](https://www.mcst.ru/LCC)
- [Официальные загрузки и целевые пакеты LCC](https://dev.mcst.ru/download/)

Изменения протокола проходят review в Fragile-Baby. Изменения ABI/manifest повышают schema_version и проходят обратную проверку контрактов. Версия протокола не означает автоматически реализованные функции.
