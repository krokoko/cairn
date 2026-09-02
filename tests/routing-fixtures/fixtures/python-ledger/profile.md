# Python ledger fixture profile

Minimal profile: Python payment ledger with integer balance operations.

## Signals

- `src/ledger.py` — `transfer()`, `balance` with u64-style arithmetic
- `tests/test_ledger.py` — unit tests, no property tests
- Requirements mention conservation: total funds preserved
- No CrossHair, no Hypothesis

## Component classification

- Archetype: Deterministic library
- Bug surface: B (arithmetic / conservation)
- Criticality: High
