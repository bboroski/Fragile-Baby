# Fragile-Baby E2K qualification evidence matrix

This contract records qualification evidence without manufacturing it. The current
project maturity remains **architecture proposal / target evidence pending**.

## Evidence stages

| Stage | What it can establish | What it cannot establish |
|---|---|---|
| Host | Portable parser and metadata checks | E2K instruction or ABI compatibility |
| Cross-build | A named E2K toolchain can emit an artifact | That the artifact boots or behaves correctly |
| Emulator | Behavior under a declared emulator profile | Physical board behavior |
| Physical target | Behavior on an identified CPU/stepping/board | Qualification outside the tested configuration |

Each stage is independent. Missing evidence remains `not-tested` or `unknown`;
it is never inferred from another stage. A successful host test must not promote
an E2K target to `hardware-qualified`.

## Matrix files

- `e2k-evidence-matrix.schema.json` defines the versioned data contract.
- `e2k-evidence-matrix.example.json` is deliberately populated with unknown
  target identity and untested stages.

The matrix is a governance and reporting feature. It does not contain register
writes, boot code, microcode, voltage/frequency controls, or claims of target
support. Keep canonical repository identity as **Fragile-Baby**.
