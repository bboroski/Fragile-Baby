# E2K evidence advisor

Run:

```bash
python3 tools/evidence_advisor.py
python3 tools/evidence_advisor.py docs/qualification/e2k-evidence-matrix.example.json --json
python3 -m unittest discover -s tests -v
```

The advisor validates core matrix structure and reports sequential stage coverage, maturity consistency and the next recommended evidence action. Coverage is a count of passed stages, **not confidence or probability**. The tool never probes a CPU, invents an E2K toolchain fingerprint or promotes host evidence into emulator/physical qualification. A physical-target pass still requires complete target identity and traceable evidence references; independent review remains necessary.
