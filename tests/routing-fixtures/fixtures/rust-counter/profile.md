# Rust counter fixture profile

Minimal profile: Atomic seat counter guarded by Mutex.

## Signals

- `src/counter.rs` — single `Mutex<u32>` increment/decrement
- Unit tests, clippy, no formal methods

## Classification

- Archetype: Deterministic library
- Bug surface: A (local invariant)
- Criticality: Low
