# Verifier-Guided Search

## Core rule

**An LLM evaluator may critique. It must not be the final correctness authority when a
deterministic verifier is available.**

Autonomous coding agents need a search architecture, not merely a dual-agent review loop.
The pattern separates four roles:

| Role | Responsibility | Must be deterministic? |
|------|----------------|------------------------|
| **Candidate generator** | Produces implementation or patch variants | No (LLM) |
| **Verifier** | Accepts or rejects against immutable specification | **Yes** |
| **Search strategy** | Selects next candidates from verifier feedback | Prefer deterministic |
| **Evidence store** | Records verdicts, counterexamples, artifacts | Yes |

## Architecture

```text
                    immutable specification
                            │
                            ▼
                     Candidate solution
                            │
                            ▼
                   Deterministic verifier
                            │
                 ┌──────────┴──────────┐
                 │                     │
              PASS                   FAIL
                 │                     │
                 ▼                     ▼
              evidence       counterexample / trace
                                       │
                                       ▼
                                Search strategy
                            ┌──────────┼──────────┐
                            ▼          ▼          ▼
                         Candidate A Candidate B Candidate C
                            │          │          │
                            └──────────┼──────────┘
                                       │
                                       ▼
                                    verifier
```

Ranking multiple passing candidates follows `candidate-selection-policy.md` (canonical rule).

## Search patterns

| Pattern | Mechanism | Best for | Cost |
|---------|-----------|----------|------|
| **Generate → Verify → Retry** | Single agent fixes until verifier passes | Simple agent correction loops | Low–medium |
| **Best-of-N + verifier** | N independent implementations; keep those passing verifier | Explore independent solution directions | N× generation |
| **Counterexample-guided refinement** | Verifier counterexample feeds next prompt | Solver/test feedback is informative | Medium |
| **Beam / Top-K** | Keep K best partial solutions; expand each | Multiple plausible directions | K× verification |
| **Multi-island search** | Parallel populations with periodic migration | Avoid local minima; preserve architectural diversity | High |
| **Pareto search** | Non-dominated set across correctness + secondary metrics | Correctness + performance + maintainability | High |
| **Adaptive search** | Switch strategy when progress stalls (e.g. beam → islands) | Long-running autonomous tasks | Variable |

## When to apply

| Signal | Recommend verifier-guided search |
|--------|----------------------------------|
| L4/L5 autonomy target on component | Yes — search without deterministic authority is unsafe |
| Deterministic verifier exists (tests, types, model checker, symbolic tool) | Yes — use it as authority |
| High-criticality change with machine-checkable spec | Yes |
| Only LLM-as-judge available | No — use dual-agent patterns; flag as autonomy cap |
| Low-criticality utility code | Optional — standard CI may suffice |

## Verifier types (by strength)

| Verifier | Examples | Counterexample quality |
|----------|----------|------------------------|
| Type checker | `tsc`, `mypy`, `rustc` | Compiler error with location |
| Test suite | `pytest`, `cargo test` | Failing assertion + stack trace |
| Property test | Hypothesis, proptest | Shrunk counterexample input |
| Symbolic / contract | CrossHair, Dafny, Kani | Concrete violating input |
| Model checker | TLC, Apalache, Quint | Trace violating invariant |
| Differential | Old vs new on shared inputs | Diverging input + outputs |
| Formal proof | Lean, Coq, Verus | Proof obligation or countermodel |

Prefer verifiers that emit **actionable counterexamples** — they drive search more effectively
than boolean pass/fail.

## Orchestration tools (external harnesses)

Cairn prescribes patterns; execution lives in complementary harnesses:

| Tool | Role |
|------|------|
| SkyDiscover (unverified source) | Candidate/evaluator/search separation; Best-of-N, beam, islands |
| GEPA, OpenEvolve, ShinkaEvolve | Evolutionary / program-search loops with verifier feedback |
| lemmafit | TypeScript spec → external verifier in agent session |
| Custom CI matrix | Generate N candidates in parallel jobs; filter by test pass |

## Integration with CI

1. **Immutable spec** lives outside the agent's write scope (requirements, approved properties,
   holdout tests, formal spec with hash pinned in CI).
2. **Verifier runs server-side** — branch protection required; agent cannot skip.
3. **Search loop** may run locally or in CI; only verifier-passing candidates merge.
4. **Evidence record** per candidate: commit, verifier config hash, verdict, counterexample artifact.
5. **LLM critic** optional — produces hints, never overrides verifier failure.

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| LLM evaluator as final gate | Self-confirmation bias; no falsifiability |
| Agent-writable verifier | Oracle tampering — see `oracle-integrity.md`, AI012 |
| Combined score without mandatory tier | See `candidate-selection-policy.md` anti-patterns |
| Search without counterexample capture | Cannot improve; repeats same failure |
| Verifier only in local hooks | Agent bypasses with `--no-verify` |

## Related patterns

- `generator-evaluator.md` — dual-agent patterns when no deterministic verifier exists
- `candidate-selection-policy.md` — mandatory properties vs optimization objectives
- `oracle-integrity.md` — ensure verifiers cannot be weakened by the search agent
- `harness-architecture.md` — evidence pipeline and promotion policy
