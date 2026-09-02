# Python parser fixture profile

Minimal profile: Python binary parser on untrusted input.

## Signals

- `src/parser.py` — hand-written byte indexing, `parse_*` on arbitrary bytes
- Unit tests cover happy path only
- No fuzz target, no sanitizers on extension module

## Classification

- Archetype: Deterministic library
- Bug surface: D (untrusted input)
- Criticality: Medium–High
