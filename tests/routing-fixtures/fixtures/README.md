# Verification Routing Fixtures

Synthetic fixture repositories for evaluating Cairn verification routing accuracy.
Each fixture describes a minimal codebase profile and expected Cairn recommendations.

Run routing evals by invoking `/assess-verification` and `/design-strategy` against fixture
descriptions and comparing output to `expected-routing.json`.

## Fixtures

| Fixture | Archetype | Bug surface | Expected routing highlights |
|---------|-----------|-------------|----------------------------|
| `python-ledger` | Deterministic library | B | Hypothesis + CrossHair + arithmetic invariants |
| `python-parser` | Deterministic library | D | Fuzzing + property round-trips |
| `rust-counter` | Deterministic library | A | Types + unit tests; must not add formal methods |
| `rust-distributed-service` | Distributed/stateful | C2 | Turmoil/MadSim DST + integration tests |
| `distributed-protocol` | Distributed/stateful | C3 | P/Quint/TLA+ model checking + model-based conformance |
| `c-to-rust-migration` | Legacy monolith | B+D | Differential + translation validation (C2Rust pattern) |
| `agentic-payment-agent` | Agentic application | B+C3 | Tool policy + temporal invariants + Skylos + runtime trace conformance |

## Metrics (target — not computed by any harness yet)

No script computes these. They define what a future eval harness would report when it compares real
skill output against `expected-routing.json`.

| Metric | Description |
|--------|-------------|
| Routing accuracy | % fixtures where primary tool recommendations match expected |
| Oracle identification recall | % expected oracle types identified |
| Over-verification rate | % fixtures where ceremony-risk correctly flagged |
| Missing critical oracle rate | % expected gaps missed |

## Usage

1. Read fixture `profile.md` and `expected-routing.json`
2. Run assessment skill against profile description
3. Compare report routing to expected
4. Track regressions when plugin knowledge changes

Validate fixture layout, schema conformance, and that every expected tool exists in the plugin references (this does **not** measure routing accuracy):

```bash
mise run test:fixtures
```

Fixtures live under `tests/` so they are not shipped with the installed plugin.
