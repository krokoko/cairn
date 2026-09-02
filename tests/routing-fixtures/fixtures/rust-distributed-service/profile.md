# Rust distributed service fixture profile

Async Rust service with network RPC, retries, and leader election hints.

## Signals

- `src/` — `tokio`, `async` RPC handlers, retry logic
- No Turmoil/MadSim, no formal spec
- Integration tests with testcontainers only

## Classification

- Archetype: Distributed/stateful
- Bug surface: C → **C2** (distributed implementation)
- Criticality: High
