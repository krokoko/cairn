# Verification Taxonomy

## Method selection

Select methods by claim and failure surface. There is no method-wide assurance score: a proof
of the wrong proposition can be less useful than a relevant regression example. Use
`evidence-semantics.md` to interpret results and `method-failure-modes.md` for prerequisites.
Cost and automation depend on the configured scope, ecosystem, and existing expertise.

### Testing and generative methods

| Method | Key tools | Evidence mode | Useful scope / limit |
|--------|-----------|---------------|----------------------|
| Unit testing | pytest, Jest, go test | Sampled execution | Scoped cases; assertions decide what is checked |
| BDD / executable specs | Cucumber, Behave, godog | Sampled execution | Reviewed acceptance rules; scenario declarations alone are not runs |
| Integration testing | testcontainers, supertest | Sampled execution | DB/API/queue interactions; qualify environment fidelity |
| System testing | End-to-end frameworks | Sampled execution | Customer workflows; tested paths and conditions only |
| Property-based testing | Hypothesis, fast-check, proptest | Sampled exploration | Generated cases of round-trips, ordering, idempotence; review properties/generators |
| Fuzzing | libFuzzer, AFL, cargo-fuzz | Sampled exploration | Parsers/codecs; semantic checks require an oracle beyond crashes |
| Consumer-driven contracts | Pact, Spring Cloud Contract | Sampled/contract checks | Reviewed consumer expectations within provider/version scope |
| Behavioral twin testing | Service clones, scenario runners | Sampled execution | Tests a dependency model; fidelity to the real provider needs evidence |
| Approval / characterization testing | ApprovalTests, insta, snapshots | Sampled comparison | Preserve reviewed behavior; a baseline can contain bugs |
| Regression replay | Captured inputs/outputs, golden traces | Sampled comparison | Historical cases with approved outputs and relevant environments |
| Mutation testing | mutmut, Stryker, cargo-mutants | Diagnostic campaign | Sensitivity to selected violating edits; investigate equivalent mutants |

### Static and formal methods

| Method | Key tools | Evidence mode | Useful scope / limit |
|--------|-----------|---------------|----------------------|
| Linters/SAST | ESLint, ruff, Semgrep, clippy | Static rules/search | Configured patterns; soundness and missed cases vary |
| Type systems | TypeScript strict, mypy, Rust | Static properties | Language/checked subset and escape hatches limit guarantees |
| Profiling | pprof, perf, py-spy | Diagnostic measurement | Performance under the measured workload; not functional correctness |
| Sanitizers | ASan, TSan, UBSan, MSan | Instrumented execution | Supported error classes on executed native/unsafe paths |
| Contracts (DbC) | icontract, JML, assertions | Runtime checks or proof | Reviewed pre/postconditions; distinguish execution from static discharge |
| Abstract interpretation | Astree, Frama-C/EVA | Static analysis | Supported semantics/environment; unresolved alarms need interpretation |
| Schedule exploration | Loom, Shuttle, Coyote | Bounded or sampled exploration | Instrumented concurrency; record bound and exhaustive versus randomized mode |
| Formal spec + model checking | TLA+/TLC, Alloy, Stateright | Model exploration | Completed model scope; implementation correspondence remains an obligation |
| SMT / bounded verification | Kani, Z3 encodings | Bounded analysis | Completed obligations, bounds, unwinding, and assumptions |
| Deductive verification | Dafny, SPARK, Frama-C/WP | Proof | Stated propositions and trusted toolchain, not all stakeholder needs |
| Theorem proving | Lean, Coq/Rocq | Proof | Formalized semantics, assumptions, and connection to shipped artifacts |
| Symbolic execution | KLEE, angr, Mythril | Search or bounded analysis | Report tool/mode guarantees; path search alone is not exhaustive proof |
| Statistical model checking | PRISM, Monte Carlo methods | Statistical analysis | Model, sampling assumptions, confidence/error bounds |

### Operational and human methods

| Method | Key tools | Evidence mode | Useful scope / limit |
|--------|-----------|---------------|----------------------|
| Agentic manual testing | Playwright, CDP, shell + QA charters | Observed workflows | Acceptance or validation purpose depends on the question |
| Runtime verification | Monitors, RV-Monitor | Trace monitoring | Recorded events and ordering; detection needs a separate enforcement mechanism |
| Shadow testing | Traffic mirroring | Sampled comparison | Compared traffic, side effects, reference quality, and tolerance |
| Canary / progressive delivery | Argo Rollouts, feature flags | Operational observation | Exposed cohort, signals, thresholds, rollback coverage |
| Chaos engineering | Chaos Monkey, Litmus | Fault campaign | Tested hypotheses/faults and monitored invariants |
| LLM-as-Judge evaluation | Model scoring against rubrics | Statistical/heuristic judgment | Independently labeled calibration, model/rubric version, bias |
| Provenance / attestation | in-toto, SLSA, Sigstore/Cosign | Provenance | Authenticates records about artifact/process; not behavioral correctness |
| Human review | Code/intent review, user studies | Reviewed/observed outcomes | Reviewer/task context and recorded decision, not universal correctness |

## Oracle types

| Oracle | Applicable when | Example |
|--------|-----------------|---------|
| Exact | Deterministic function, known I/O pairs | `sort([3,1,2]) == [1,2,3]` |
| Metamorphic | Transformations have known effects | `search(q) ⊆ search(broader_q)` |
| Differential | Multiple implementations to compare | Old vs new version |
| Contract | API/interface must obey a schema or protocol | Response matches OpenAPI spec; pre/postconditions hold |
| Temporal | State transitions must follow ordering/protocol rules | `open → close` legal, `close → close` rejected |
| Statistical | Bounded stochastic output | Accuracy > 0.95, p99 < 200ms |
| Performance envelope | Measurable load/latency/resource bounds | p99 < 100ms under 10k req/s, memory < 512MB |
| Replay | Historical inputs with validated outputs | Production traces as regression |
| LLM-as-Judge | Non-deterministic output, human review too slow | Generated docs, UI copy, refactoring quality |
| Human | Requires domain judgment | UX quality, ambiguous correctness |
| Behavioral twin | Third-party integrations needing real-behavior verification | Clone of external service exercised via scenarios |

Attestation/provenance (in-toto, SLSA) is deliberately **not** in this table: it records *what
ran on which commit with what verdict* and signs it — it packages evidence, it does not adjudicate
output correctness. Treat it as an evidence rail, not an oracle.

## Oracle strength

Load `oracle-lifecycle.md`. Evaluate adequacy, sensitivity, independence, and semantic freshness
against the bounded claim; machine-checkability or determinism alone does not establish strength.

| Strength | Meaning for the assessed claim |
|----------|--------------------------------|
| Qualified | Relevant current review, sensitivity controls, and independence/fidelity evidence support the claim |
| Weak | A demonstrated adequacy, sensitivity, independence, or freshness gap limits the oracle |
| Unknown | Necessary evidence was not inspected; do not label an unexamined oracle strong or absent |
| None | No applicable oracle found in the inspected scope |

Properties, examples, and recorded references can all encode obsolete intent. Mutation challenges
sensitivity to selected edits, not business-rule freshness. A property-based campaign is useful
when reviewed invariants and generators explore failures that examples leave uncovered.
