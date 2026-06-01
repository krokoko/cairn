# Method Failure Modes

What can go wrong with each verification method. Use this to warn about risks when
recommending methods and to identify false confidence in existing verification.

## Testing methods

| Method | Failure modes | Prerequisites |
|--------|--------------|---------------|
| Unit testing | Misses interface, config, timing, and distributed-state bugs | Seams, deterministic fixtures, stable inputs |
| Integration testing | Flaky if environments are poorly controlled; still misses production-only issues | Realistic fixtures, schemas, side-effect management |
| System testing | Expensive, slow, prone to flakiness; weak at isolating causes | Deployment-like environments, stable acceptance criteria |
| Property-based testing | Weak generators or weak properties create false confidence; poor shrinking hurts debugging | Invariants easier to state than enumerate |
| Fuzzing | Strong for crashes but weak for semantic correctness unless paired with assertions | Seed corpus, harness quality, sanitizers |
| Regression replay | Only protects what is already covered; accretes brittle tests | Historical failing cases, captured workflows |
| Approval / characterization testing | Snapshot churn; approving a bad baseline locks in the current (possibly wrong) behavior | Stable I/O edges, diff-friendly serialization, disciplined re-approval |
| Mutation testing | Slow on large codebases; equivalent mutants create noise | Existing test suite to evaluate |

## Static and formal methods

| Method | Failure modes | Prerequisites |
|--------|--------------|---------------|
| Linters/SAST | High false-positive/negative variance depending on rule quality | Rule hygiene, project conventions |
| Type systems | Only proves what the type system can express; `any`-like escapes weaken value | Disciplined annotations, boundary hygiene |
| Profiling | Finds bottlenecks, not semantic correctness; misleads if workloads are unrealistic | Representative workloads |
| Sanitizers | Only sees executed paths; adds overhead; poor coverage = false negatives | Compatible toolchains, test/fuzz workloads |
| Contracts (DbC) | Weak or inaccurate contracts create correctness theater; runtime-only misses unexecuted paths | Explicit invariants, ownership of semantics |
| Abstract interpretation | Precision loss creates too many alarms; domain tuning is hard | Sound semantics, language/tool support |
| Schedule exploration | State explosion; harness not representative of production integration; only exhaustive (Loom) up to a bound, randomized (Shuttle) gives no completeness guarantee | Instrumented concurrency primitives, bounded scope |
| Model checking | State explosion is the classic limit; finite abstractions miss bugs outside scope | Explicit state models, checkable properties |
| SMT solving | Fragile encodings, solver timeouts, quantifier pain, assumption mistakes | Good specs, loop bounds or invariants |
| Deductive verification | Annotation burden is high; proof breakage under code change; specs may be weaker than intent | Contracts, loop invariants, framing |
| Theorem proving | Highest labor; strong dependence on prover skill and library maturity | Formalized semantics, proof engineering |
| Symbolic execution | Path explosion for large programs; environment modeling is hard | Bounded scope, concrete entry points |

## Operational methods

| Method | Failure modes | Prerequisites |
|--------|--------------|---------------|
| Runtime verification | Monitor overhead, spec quality, observability gaps, signal noise | Event instrumentation, executable properties |
| Shadow testing | Candidate and baseline can diverge for benign reasons; write paths need isolation | Traffic mirroring, comparable observability |
| Canary delivery | Weak metrics or wrong thresholds let bad versions through; too-small samples | Observability, rollback paths, release policy |
| Chaos engineering | Can cause real incidents if blast radius is unmanaged; poor hypotheses = random breakage | Steady-state metrics, safety controls, rollback |
| Human review | Slow, inconsistent, hard to scale; becomes superficial if not targeted | Clear escalation criteria, evidence summaries |

## The false-confidence trap

Incomplete invariants can produce automated confidence in incorrect behavior. A proof
that the code satisfies the wrong property is still the wrong system. Always pair
formal evidence with operational validation. Assurance is relative to a property, a
model, a specification, and a trusted toolchain.

## Development-stage recommendations

| Stage | Primary methods | Rationale |
|-------|----------------|-----------|
| Design | Contracts, formal specs, model checking | Catch design bugs before code exists |
| Implementation | Static analysis, unit/integration, property tests, fuzzing | Fast feedback on code correctness |
| Pre-release | System/regression suites, profiling, sanitizers, shadow | Validate in realistic conditions |
| Production | Canaries, runtime monitors, chaos, human escalation | Catch what labs miss |
