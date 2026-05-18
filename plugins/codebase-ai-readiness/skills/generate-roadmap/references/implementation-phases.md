# Implementation Phases

## Five-phase strategic model

Roadmaps should follow this incremental sequence. Each phase builds on the previous.

### Phase 1: Make semantics explicit

Add contracts, schemas, invariants, and risk classes to interfaces you care about.
If you cannot state the property, you cannot automate its verification.

**Actions**: Add OpenAPI/protobuf, typed boundaries, assertion contracts, config schemas.
**Unlocks**: Machine-checkable obligations for tools to consume.

### Phase 2: Industrialize the fast loop

Every change should trigger static checks, tests, regression replay, property tests,
and sanitizers. Output should be uniform evidence, not just console text.

**Actions**: CI branch protection, required checks, coverage thresholds, linting in CI,
property-based tests for stable invariants, structured test output.
**Unlocks**: Agents can iterate freely and get fast, deterministic feedback.

### Phase 3: Add deep evidence where asymmetry justifies it

Bring formal methods only where failure cost, concurrency, or nondeterminism justify
the investment. Do not try to "formally verify the whole product."

**Actions**: TLA+ for protocols, model checking for state machines, SMT for critical
algorithms, theorem proving only for smallest trusted kernels.
**Unlocks**: High confidence on critical paths without over-investing on low-risk code.

### Phase 4: Close the loop with reality

Build feedback from production back into the verification pipeline. Lab evidence
alone is insufficient.

**Actions**: Replay labels from incidents, shadow evaluation, canary analysis, runtime
monitors for temporal properties, held-out validation.
**Unlocks**: Catches spec drift and environment mismatches that testing alone misses.

### Phase 5: Reposition humans as exception handlers

Humans should define semantics, review the harness, adjudicate ambiguous cases, and
approve high-blast-radius deploys. They should not be the primary scalability mechanism.

**Actions**: Risk-based approval gates, escalation criteria, human review only for
low-confidence or high-impact changes, structured evidence summaries for reviewers.
**Unlocks**: Autonomous iteration for routine work; human focus on architecture and edge cases.

## Six strategic principles

Use these to guide prioritization within any roadmap:

1. **Contracts and replay as common currency** — every interface gets invariants; every bug becomes a replayable regression
2. **Property-based testing before heavy proofs** — cheapest way to make a component verifiable
3. **Make CI evidence-driven** — structured evidence feeds decisions, not informal norms
4. **Formal methods only where justified** — protocols, allocators, codecs, security boundaries
5. **Shadow/canary as verification, not just release** — bridge from "model says okay" to "reality confirms"
6. **Instrument the harness itself** — track flakiness, solver timeouts, label drift, human override rates

## Property-based testing as the bridge method

Property-based testing is the most important bridge method for autonomous construction.
It is much cheaper than full proof, but far more scalable than hand-written examples
when the abstraction has crisp invariants. Prioritize it before adding heavy tooling.

**Best for**: round-trips, associativity, ordering, monotonicity, idempotence, codec
equivalence, cache coherence, CRDT laws, commutativity, serialization stability.
