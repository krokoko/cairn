# C to Rust migration fixture profile

Minimal profile: Porting a C library to Rust with C2Rust as reference.

## Signals

- `legacy/foo.c` — original implementation
- `src/foo.rs` — migrated Rust via C2Rust + manual cleanup
- Characterization tests from C golden outputs
- Active migration PRs, no differential CI gate

## Classification

- Archetype: Legacy monolith
- Bug surface: B+D (conservation + parsing)
- Change mode: language port / migration
- Criticality: High
