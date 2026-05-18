# Oracle Patterns

## Oracle taxonomy

| Type | Definition | Strengths | Weaknesses |
|------|-----------|-----------|------------|
| Exact | Known input/output pairs | Highest confidence | Doesn't scale to large input spaces |
| Metamorphic | Relations between executions | No need for exact answers | Weak relations give weak assurance |
| Differential | Compare multiple implementations | Catches divergence | Requires reference impl |
| Statistical | Bounded distributions/thresholds | Handles stochastic behavior | Not proof of correctness |
| Replay | Historical inputs with validated outputs | Reality-grounded | Stale if system evolves |
| Performance envelope | Measurable load/latency/resource bounds | Machine-checkable; prevents perf regressions | Doesn't verify functional correctness |
| LLM-as-Judge | Separate model scores output against rubric | Cheaper than human, handles ambiguity | Biases (position, verbosity, self-preference); needs calibration |
| Human | Domain expert judgment | Handles ambiguity | Slow, expensive, inconsistent |
| Behavioral twin | High-fidelity clone of external service | Tests real behavior, not assumptions; holdout scenarios prevent agent gaming | Requires building/maintaining clone; fidelity drift |

## When to use each oracle

| Oracle | Use when | Pattern | Examples |
|--------|----------|---------|----------|
| Exact | Deterministic, enumerable inputs | `assert f(input) == expected` | Sorting, parsing, encoding |
| Metamorphic | Known relations between I/O | `assert f(shuffle(x)) == f(x)` | Search, compilers, ML |
| Differential | Reference impl exists | `assert new(x) == old(x)` | Rewrites, migrations, ports |
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

Position bias, verbosity bias, self-preference bias, authority bias. Use different model family than generator; calibrate against 50-100 human-labeled gold examples before deployment.

### Human oracle

Route low-confidence outputs to human review queue with structured evaluation criteria. Use only when no automated or LLM-based method can assess correctness.

### Behavioral twin pattern

A behavioral twin is a high-fidelity clone of an external service (SaaS API, third-party system) built specifically for testing. Unlike interface mocks (which verify assumptions) or contract tests (which verify schemas), twins verify **actual behavioral compatibility**.

**When to recommend:**
- Codebase integrates with 3+ external services
- Integration code is agent-written (high plausible fabrication risk)
- Interface mocks exist but integration bugs still reach production
- Rate limits or costs prevent testing against real services at scale

**Architecture:**
- Twin built from public API docs + SDK compatibility targets
- Self-contained binary (no network dependencies)
- Scenarios stored externally as holdout sets (agents cannot access or game them)
- Verification measured as satisfaction (probabilistic) not boolean pass/fail

**Key distinction from mocking:**

| Approach | Verifies | Agent can game? | Catches fabrication? |
|----------|----------|-----------------|---------------------|
| Interface mocks | Code structure | Yes | No |
| Contract tests | Schema compliance | Partially | Partially |
| Behavioral twins | End-to-end scenario satisfaction | No (holdout) | Yes |

## Converting implicit oracles to explicit ones

| Implicit pattern | Explicit conversion |
|-----------------|---------------------|
| "It looks right" | Define specific properties to check |
| "No one complained" | Add monitoring + alerting thresholds |
| "Manual QA passed" | Capture QA criteria as automated checks |
| "Same as before" | Add snapshot/differential testing |
| "Meets requirements" | Encode requirements as contracts or schemas |
