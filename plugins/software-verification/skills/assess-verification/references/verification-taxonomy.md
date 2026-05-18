# Verification Taxonomy

## Method ratings

Ratings: VH=Very High, H=High, M=Medium, L=Low. Columns: Assurance / Cost / Automation / Scalability / Expertise.

### Testing and generative methods

| Method | Key tools | Ratings (A/C/Au/S/E) | When to use |
|--------|-----------|----------------------|-------------|
| Unit testing | pytest, Jest, go test | M / L / H / H / L | Per-PR baseline; deterministic, scoped logic |
| Integration testing | testcontainers, supertest | M / M / H / M / M | Cross-boundary interactions (DB, APIs, queues) |
| System testing | End-to-end frameworks | M-H / H / M / L-M / M | Release gates, customer-visible workflows |
| Property-based testing | Hypothesis, fast-check, proptest | H / M / H / H / M | Clear invariants: round-trips, ordering, idempotence |
| Fuzzing | libFuzzer, AFL, cargo-fuzz | M-H / M / H / H / M | Parsers, codecs, security-sensitive inputs |
| Regression replay | Captured inputs/outputs | M / L-M / H / H / L | Every bug becomes a permanent test case |
| Mutation testing | mutmut, Stryker, cargo-mutants | M / M / H / M / M | Assessing test suite quality and strength |

### Static and formal methods

| Method | Key tools | Ratings (A/C/Au/S/E) | When to use |
|--------|-----------|----------------------|-------------|
| Linters/SAST | ESLint, ruff, Semgrep, clippy | L-M / L / H / H / L | First static gate for every repo |
| Type systems | TypeScript strict, mypy, Rust | M-H / L-M / H / H / M | Everywhere; cheapest bug-class elimination |
| Profiling | pprof, perf, py-spy | L(func), M(perf) / L-M / H / H / M | Performance budgets, regression detection |
| Sanitizers | ASan, TSan, UBSan, MSan | H / L-M / H / H / L-M | Mandatory for native/unsafe code |
| Contracts (DbC) | icontract, JML, assertions | M-H / M / H / H / M | Interface semantics; first step to formal |
| Abstract interpretation | Astree, Frama-C/EVA | H / H / H / M / H | Safety-critical embedded, numeric code |
| Formal spec + model checking | TLA+/TLC, Alloy, Stateright | H-VH / M-H / H / M-L / H | Protocols, distributed state, concurrency |
| SMT / bounded verification | Kani, Dafny, Z3 | H / M / H / M / H | Bit-precise kernels, arithmetic invariants |
| Deductive verification | Dafny, SPARK, Frama-C/WP | H-VH / H / M-H / M / H | Critical algorithms, codecs, memory safety |
| Theorem proving | Lean, Coq/Rocq | VH / VH / L-M / L / VH | Crypto, verified compilers, protocol cores |
| Symbolic execution | KLEE, angr, Mythril | M-H / M-H / H / M / H | Security analysis, smart contracts, path coverage |
| Statistical model checking | PRISM, Monte Carlo methods | M-H / M / H / H / H | Randomized protocols, reliability, queuing |

### Operational and human methods

| Method | Key tools | Ratings (A/C/Au/S/E) | When to use |
|--------|-----------|----------------------|-------------|
| Runtime verification | Monitors, RV-Monitor | M-H / M / H / M / H | Temporal protocols, API usage rules |
| Shadow testing | Traffic mirroring | H / M / H / H / M | Rewrites, replacements, before promotion |
| Canary / progressive delivery | Argo Rollouts, feature flags | M-H / M / H / H / M | All production-facing releases |
| Chaos engineering | Chaos Monkey, Litmus | M / M / M / M / M | Distributed systems, failover paths |
| Human review | Code review, approvals | Variable / M / M / M / M | High-risk, ambiguous, low-confidence changes |

## Oracle types

| Oracle | Applicable when | Example |
|--------|-----------------|---------|
| Exact | Deterministic function, known I/O pairs | `sort([3,1,2]) == [1,2,3]` |
| Metamorphic | Transformations have known effects | `search(q) ⊆ search(broader_q)` |
| Differential | Multiple implementations to compare | Old vs new version |
| Statistical | Bounded stochastic output | Accuracy > 0.95, p99 < 200ms |
| Replay | Historical inputs with validated outputs | Production traces as regression |
| Human | Requires domain judgment | UX quality, ambiguous correctness |

## Key insight

Property-based testing is the most important bridge method for autonomous construction:
cheaper than proof, far more scalable than hand-written examples when invariants are crisp.
