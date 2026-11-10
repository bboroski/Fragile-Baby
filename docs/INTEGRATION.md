# SAMBU ecosystem integration contracts

Fragile-Baby owns the Elbrus Linux target layer. It does not absorb the responsibilities or source trees of the other repositories into a monolith. Each project stays independently buildable and exposes only the capabilities it owns.

## Dependency direction

```text
                  SAMBU / Klipot
              build policy + metadata
                         |
              Fragile-Baby (e2k target)
                         |
                 Linux / MCST LCC
                         |
                  Elbrus processor

     Application composition (explicit, optional adapters)
       |             |              |               |
     Kloz            CO           SaintSI       ReaperCripple
 platform ABI     lifecycle       assurance      BSP/fixtures

     ToolNG: separate Windows operator diagnostics
```

The diagram is an integration plan, not proof that every adapter is already linked. Fragile-Baby can build and test its portable core without cloning or compiling the other repositories.

## Project responsibilities

| Repository | Existing foundation verified in its source tree | Fragile-Baby integration |
|---|---|---|
| **Kloz** | C11 status ABI, fixed-capacity memory, versioned platform operations for monotonic clock, IRQ guard and device barrier | Natural low-level contract. Linux userspace can supply a monotonic clock; IRQ and device-barrier capabilities remain absent unless a kernel/firmware port proves them |
| **CO** | Allocation-free deterministic lifecycle with init/step/shutdown callbacks and partial-init cleanup | Application may own a CO runtime and pass E2K platform services through callback context. CO is not a scheduler or RTOS |
| **SaintSI** | Fixed-capacity heartbeat registry, rollover-safe timeout checks and degraded-state reporting | Observe successful CO work and target-service health. No automatic reset or watchdog feed is authorized by a heartbeat |
| **ReaperCripple** | C11 BSP family adapters, hardware profile, bounded telemetry, staged bootstrap/rollback, calibration and manufacturing records | Its current `arch_target_t` enum does not contain Elbrus/e2k. A truthful upstream E2K adapter requires an explicit architecture enum and a reviewed E2K BSP; do not map E2K to x86, ARM or RISC-V |
| **SAMBU** | Python-hosted language/tooling, module manifest contract, experimental C11 IR kernel and staged native compiler architecture | Use SAMBU for declarative build policies, capability manifests and future target-neutral IR integration. Its native E2K backend is not currently implemented; production code generation remains with MCST LCC |
| **ToolNG** | C17 Windows diagnostic application, evidence scoring and local reports | Keep its Win32 shell on Windows. A future read-only report adapter may consume build/target evidence, but it must preserve unknown vs failed and must not modify a device |
| **Klipot** | Registry projection, versioned ecosystem contracts, schema checks and browser labs | Register Fragile-Baby metadata and expose target validation status. Browser simulations must not be presented as hardware evidence |
| **NUN / NUNLauncher** | Current registry classifies both as documentation scaffolds without kernel/loader implementation | Keep any future OS boot integration behind a separate boot protocol. Fragile-Baby is a Linux userspace platform layer, not a bootloader or OS kernel |

## Integration rules

- Keep dependencies acyclic. The platform layer must not depend on a higher-level policy/runtime module.
- Use fixed-width fields, explicit structure sizes/versions and caller-owned state at C ABI boundaries.
- Use the Kloz clock contract only when a valid monotonic tick source is configured. Linux userspace time is not a CPU cycle counter.
- Publish CO progress to SaintSI only after a completed successful work step.
- Keep ReaperCripple board profiles authoritative for exact silicon, board revision, calibration and manufacturing evidence.
- Treat ToolNG reports and Klipot dashboards as evidence presentation, not a grant of hardware authority.
- Keep SAMBU compiler backend status explicit; do not label an IR model or build manifest as native code generation.

## Current integration status

The public C11 platform API and Linux E2K probe are implemented inside Fragile-Baby. Cross-repository adapters remain optional integration work. In particular, ReaperCripple needs an upstream E2K enum/BSP extension before Fragile-Baby can claim a native ReaperCripple E2K adapter.
