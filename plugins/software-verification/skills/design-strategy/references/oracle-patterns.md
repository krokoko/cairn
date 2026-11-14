# Oracle Patterns

## Oracle taxonomy

| Type | Definition | Strengths | Weaknesses |
|------|-----------|-----------|------------|
| Exact | Approved input/output pairs | Precise verdict for exercised cases | Expected values may be wrong or stale; limited input scope |
| Metamorphic | Relations between executions | No need for exact answers | Weak relations give weak assurance |
| Differential | Compare under an approved equivalence relation | Catches divergence | A reference may preserve bugs; agreement is not general equivalence |
| Contract | Conformance to a schema or protocol | Machine-checkable; guards API boundaries | Verifies shape/protocol, not business correctness |
| Temporal | Legal state transitions and event ordering | Catches illegal sequences and protocol violations | Requires an explicit state/protocol model |
| Statistical | Bounded distributions/thresholds | Handles stochastic behavior | Not proof of correctness |
| Replay | Historical inputs with validated outputs | Reality-grounded | Stale if system evolves |
| Performance envelope | Measurable load/latency/resource bounds | Machine-checkable; prevents perf regressions | Doesn't verify functional correctness |
| LLM-as-Judge | Separate model scores output against rubric | Cheaper than human, handles ambiguity | Biases (position, verbosity, self-preference); needs calibration |
| Human | Domain expert judgment | Handles ambiguity | Slow, expensive, inconsistent |
| Behavioral twin | Maintained approximation of an external service | Exercises selected dependency behavior locally | Fidelity, supported scenarios, version drift, and feedback leakage |

## When to use each oracle

**Selection rule**: choose complementary checks for the claim and failure surface. Prefer inexpensive
checks where they answer the question; retain integration or domain review where a local oracle
cannot establish environment fidelity or intent. No oracle type has universally highest assurance.

| Oracle | Use when | Pattern | Examples |
|--------|----------|---------|----------|
| Exact | Deterministic, enumerable inputs | `assert f(input) == expected` | Sorting, parsing, encoding |
| Metamorphic | Known relations between I/O | `assert f(shuffle(x)) == f(x)` | Search, compilers, ML |
| Differential | Reference impl exists | `assert new(x) == old(x)` | Rewrites, migrations, ports |
| Contract | API obeys schema/protocol | `assert conforms(response, schema)` | REST/gRPC APIs, library interfaces |
| Temporal | State transitions must follow rules | `assert legal(prev_state, event, next_state)` | State machines, workflows, protocols |
| Statistical | Stochastic but bounded | `assert mean(results) in CI` | ML inference, load balancers |
| Replay | Historical data with known-good outputs | `assert new(trace.input) ≈ trace.output` | API migrations, model upgrades |
| Performance envelope | Performance constraints must hold | `assert p99 < 100ms, mem < 512MB` | APIs, pipelines, real-time |
| LLM-as-Judge | Non-deterministic, human review too slow | `assert judge(output, rubric) >= threshold` | Docs quality, style, UX copy |
| Human | Domain judgment required | Route to review queue with criteria | Content moderation, design |
| Behavioral twin | Third-party integrations, agent-written code | `assert twin(request) ≈ production(request)` | API integrations, SaaS connectors |

### Metamorphic relations catalog

- Permutation: `sort(shuffle(x)) == sort(x)`
- Monotonicity: `if input grows, output grows (or shrinks)`
- Inclusion: `search(specific) ⊆ search(general)`
- Idempotence: `f(f(x)) == f(x)`
- Inverse: `decode(encode(x)) == x`

### LLM-as-Judge biases to mitigate

Position bias, verbosity bias, self-preference bias, authority bias. Calibrate against independently
labeled accepted and rejected outcomes representative of the task; report sample size and uncertainty.
A different model family can diversify mistakes but does not establish independence. Keep evaluation
labels separate from optimization feedback where practical and record repeated exposure.

### Human oracle

Use domain review for intended outcomes, consequential ambiguity, and specification changes. Define
criteria and ownership; automate mechanical checks without assuming they replace this judgment.

### Behavioral twin pattern

A behavioral twin approximates an external service for repeatable tests. Its supported behavior
needs comparison with independent provider documentation, recorded interactions, or permitted live
checks. Contract tests may cover behavior as well as schemas. Neither tool name establishes fidelity.

**When to recommend:**
- Dependency behavior is important and difficult to exercise reliably
- Integration code is agent-written (high plausible fabrication risk)
- Interface mocks exist but integration bugs still reach production
- Rate limits or costs prevent testing against real services at scale

**Architecture:**
- Twin built from public API docs + SDK compatibility targets
- Self-contained binary (no network dependencies)
- Versioned scenarios include provider versions, supported operations, and explicit exclusions
- Separate evaluation cases reduce direct exposure; repeated feedback can still leak them
- Record per-scenario outcomes and sampling limits; do not imply deployed compatibility from local passes

**Key distinction from mocking:**

| Approach | Potential evidence | Important limit |
|----------|--------------------|-----------------|
| Interface mocks | Calls conform to configured expectations | Shared invented expectations can pass |
| Contract tests | Exercised schema/protocol/consumer agreements | Missing interactions and untested provider behavior |
| Behavioral twins | Exercised scenarios against modeled dependency behavior | Approximation, drift, and correlated oracle mistakes |

## Oracle lifecycle

Load `../../assess-verification/references/oracle-lifecycle.md` to assess adequacy, sensitivity,
independence, and freshness separately. Design versioned relationship review, independent expectations,
known-good/bad controls, and incident/old-versus-fixed regression evidence for consequential claims.
A new run refreshes execution evidence, not semantic approval; mutation cannot detect stale intent.
Use `../../assess-verification/references/evidence-semantics.md` to report the resulting evidence.

## Converting implicit oracles to explicit ones

| Implicit pattern | Explicit conversion |
|-----------------|---------------------|
| "It looks right" | Define specific properties to check |
| "No one complained" | Add monitoring + alerting thresholds |
| "Manual QA passed" | Capture QA criteria as automated checks |
| "Same as before" | Add snapshot/differential testing |
| "Meets requirements" | Encode requirements as contracts or schemas |
