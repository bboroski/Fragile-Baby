# Qualification chronology and evidence gates

The timeline advisor extends the E2K evidence matrix with timestamped stage records. It requires evidence identifiers for passed stages, rejects timezone-naive timestamps, checks stage progression, and refuses a hardware-qualified claim when the host → cross-build → emulator → physical-target path is incomplete.

A hash or record identifier documents integrity/traceability; it does not authenticate a publisher or prove that the target hardware was tested. Host and emulator evidence must never be substituted for physical-target evidence.

The 666-event source text is incomplete and is not used as a qualification dataset. Run `python -m unittest discover -s tests -v`.
