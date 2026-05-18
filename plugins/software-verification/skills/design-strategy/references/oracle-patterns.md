# Oracle Patterns

## Oracle taxonomy

| Type | Definition | Strengths | Weaknesses |
|------|-----------|-----------|------------|
| Exact | Known input/output pairs | Highest confidence | Doesn't scale to large input spaces |
| Metamorphic | Relations between executions | No need for exact answers | Weak relations give weak assurance |
| Differential | Compare multiple implementations | Catches divergence | Requires reference impl |
| Statistical | Bounded distributions/thresholds | Handles stochastic behavior | Not proof of correctness |
| Replay | Historical inputs with validated outputs | Reality-grounded | Stale if system evolves |
| Human | Domain expert judgment | Handles ambiguity | Slow, expensive, inconsistent |

## When to use each oracle

### Exact oracle

**Use when**: Function is deterministic, inputs are enumerable or representative, expected outputs are computable.

**Implementation pattern**:
```
assert f(input) == expected_output
```

**Examples**: Sorting, parsing, encoding/decoding, arithmetic, deterministic transformations.

### Metamorphic oracle

**Use when**: Correct output is hard to compute, but known relationships between inputs/outputs exist.

**Common relations**:
- Permutation: `sort(shuffle(x)) == sort(x)`
- Monotonicity: `if input grows, output grows (or shrinks)`
- Symmetry: `f(rotate(x)) == rotate(f(x))`
- Inclusion: `search(specific) ⊆ search(general)`
- Idempotence: `f(f(x)) == f(x)`
- Inverse: `decode(encode(x)) == x`

**Examples**: Search engines, compilers, ML models, image processing.

### Differential oracle

**Use when**: A reference implementation exists (old version, simplified version, competing library).

**Implementation pattern**:
```
assert new_impl(input) == reference_impl(input)
```

**Examples**: Rewrites, optimizations, ports to new languages, library migrations.

### Statistical oracle

**Use when**: Output is stochastic but bounded; distributions are predictable over samples.

**Implementation pattern**:
```
results = [f(random_input()) for _ in range(N)]
assert mean(results) within confidence_interval
assert p99_latency < threshold
```

**Examples**: ML inference, randomized algorithms, load balancers, cache hit rates.

### Replay oracle

**Use when**: Historical production data with known-good outcomes is available.

**Implementation pattern**:
```
for trace in historical_traces:
    assert new_system(trace.input) matches trace.validated_output (within tolerance)
```

**Examples**: API migrations, model upgrades, infrastructure changes.

### Human oracle

**Use when**: No automated method can assess correctness; domain judgment required.

**Implementation pattern**: Route low-confidence outputs to human review queue with structured evaluation criteria.

**Examples**: Content moderation, UX quality, design review, ambiguous business rules.

## Converting implicit oracles to explicit ones

| Implicit pattern | Explicit conversion |
|-----------------|---------------------|
| "It looks right" | Define specific properties to check |
| "No one complained" | Add monitoring + alerting thresholds |
| "Manual QA passed" | Capture QA criteria as automated checks |
| "Same as before" | Add snapshot/differential testing |
| "Meets requirements" | Encode requirements as contracts or schemas |
