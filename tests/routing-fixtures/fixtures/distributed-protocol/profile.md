# Distributed protocol fixture profile

Minimal profile: Raft-like consensus module with TLA+ spec on disk.

## Signals

- `spec/raft.tla` — leader election, log replication invariants
- `src/raft/` — implementation with failover tests (happy path only)
- TLC not wired in CI

## Classification

- Archetype: Distributed/stateful
- Bug surface: C → **C3** (protocol/design)
- Criticality: High
