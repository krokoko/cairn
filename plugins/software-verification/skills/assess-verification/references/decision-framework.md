# Decision Framework

## Four decision variables

| Variable | Question | Impact on method choice |
|----------|----------|------------------------|
| **Criticality** | What happens if this fails? | High -> invest in stronger assurance |
| **Determinism** | Is behavior reproducible? | Deterministic -> static/formal; non-deterministic -> operational |
| **Resources** | What expertise and time are available? | Limited -> tests + types; strong -> add formal methods |
| **Stage** | Design, implementation, pre-release, or production? | Early -> specs; late -> operational validation |

## Four strong heuristics

### 1. Critical + Deterministic

Move semantics into specifications and invest in proof-oriented methods.

**Recommended stack**: Contracts, deductive verification or SMT, property tests, theorem proving for smallest kernels.

**Typical targets**: Cryptography, parsers, codecs, allocators, arithmetic libraries.

### 2. Critical + Concurrent/Distributed

Prioritize protocol modeling, interleaving exploration, and replay.

**Recommended stack**: Formal spec (TLA+), model checking, deterministic replay/simulation, runtime verification, integration tests.

**Typical targets**: Consensus protocols, distributed state machines, queue processors, failover logic.

### 3. Input-rich but semantically local

Use generative testing and sanitizers for broad exploration.

**Recommended stack**: Property-based tests, fuzzing + sanitizers, unit tests, contracts.

**Typical targets**: Parsers, serializers, validators, file format handlers, API input processing.

### 4. Probabilistic/Learned/Environment-dependent

Rely on alternative oracles and operational validation.

**Recommended stack**: Metamorphic relations, differential evaluation, statistical thresholds, shadow testing, canaries, human escalation.

**Typical targets**: ML models, recommendation engines, search ranking, LLM-based features.

## System archetypes

| Archetype | Primary failure surface | Key methods |
|-----------|------------------------|-------------|
| Deterministic library | Logic bugs, edge cases | Property tests, fuzzing, deductive verification |
| CRUD/API service | Interface, config, regressions | Types, tests, contracts, canaries |
| Distributed/stateful | Interleavings, partial failure | Formal spec, model checking, replay, chaos |
| Safety/security kernel | Correctness of invariants | Proofs, abstract interpretation, SMT |
| ML-backed | Output quality, drift | Metamorphic, shadow, statistical, human |
| Data pipeline | Data quality, silent corruption, lineage | Golden datasets, data-quality/schema checks, metamorphic, replay |
| Infrastructure/IaC | Drift, misconfiguration, blast radius | Policy-as-code, plan validation, IaC scanning, drift detection |
| Agent-written | Trust, specification drift | Sandboxing, equivalence oracles, progressive delivery |
