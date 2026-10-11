# Hybrid Verification Strategies

## Archetype-to-stack mapping

These are candidate portfolios. Select checks for the bounded claim, bug surface, and consequence;
justify omissions and supported scope. A maturity tier never requires a method solely for its label.
Existing permission/release policy governs actions independently of verification scores.

| Archetype | Recommended stack | Why this mix works |
|-----------|-------------------|-------------------|
| Deterministic library | Types + unit tests + property tests + fuzzing + sanitizers + selective SMT/deductive | Semantics are local, input-heavy; generative methods dominate |
| CRUD/API service | Contracts/schemas + types + linters + unit/integration/regression + canaries + runtime SLOs | Most failures are interface, config, regression; proofs rarely justify ROI |
| Distributed/stateful | Formal spec + model checking + schedule exploration + deterministic replay + integration/system tests + runtime verification + canaries + chaos | Interleavings and partial failures are the hard part |
| Safety/security kernel | Contracts + deductive verification + SMT proofs + abstract interpretation + theorem proving + operational checks | Failure cost justifies proof investment; runtime catches spec mismatches |
| ML-backed | Metamorphic + differential evaluation + statistical thresholds + shadow testing + canaries + human escalation | Exact outputs unavailable; alternative oracles and operational validation dominate |
| Data pipeline | Schema/contract checks + golden datasets + data-quality assertions + metamorphic relations + replay + lineage tracking | Failures are silent data corruption, not crashes; correctness lives in the data, not the code path |
| Infrastructure/IaC | Policy-as-code + plan validation + IaC scanning + drift detection + progressive rollout + post-apply checks | Blast radius is large and reversibility low; verify before apply and detect drift after |
| Legacy monolith | Approval/characterization tests + golden-trace replay + integration smoke + baseline telemetry, then strangler-edge contracts | Freeze observable behavior before refactoring; the risk is silent regression, not greenfield design |
| Agent-written | Reviewed acceptance rules + independent controls + permitted execution + applicable delivery/recovery checks | Addresses generated changes without treating evaluation as authorization |

## Detailed recommendations per archetype

### Deterministic library

1. **Start with**: Strong types, comprehensive unit tests
2. **Add next**: Property-based tests for core invariants (round-trips, associativity, ordering)
3. **Add for native code**: Fuzzing (libFuzzer/AFL) + sanitizers (ASan, UBSan)
4. **For suitable critical claims**: Supported SMT/bounded/deductive checks with declared assumptions

### CRUD/API service

1. **Start with**: Request/response type schemas, integration tests
2. **Add next**: Contract tests at API boundaries, regression replay from production traces
3. **Add for deployment safety**: Canary analysis, runtime SLO monitoring
4. **For compliance**: Audit logging, required approval gates

### Distributed/stateful

1. **Start with**: Explicit states, transitions, and failure assumptions
2. **When interleavings justify it**: Model-check a supported protocol model (TLC, Apalache, Stateright)
3. **Add for implementation**: Schedule exploration of the real code (Loom/Shuttle), deterministic replay/simulation testing
4. **Add for production**: Runtime monitors for temporal properties, chaos experiments

### Safety/security kernel

1. **Start with**: Explicit contracts (pre/postconditions, invariants)
2. **Add next**: Deductive verification or SMT-backed proof
3. **Add for crypto/compilers**: Interactive theorem proving (Lean, Coq)
4. **For operated systems**: Monitoring with explicit event/model correspondence; detection is not enforcement

### ML-backed

1. **Start with**: Metamorphic tests (known input transformations -> expected output relations)
2. **Add next**: Shadow testing against production traffic
3. **Add for deployment**: Statistical monitoring, drift detection, canary analysis
4. **For consequential ambiguity**: Defined escalation and domain review under the project's policy

### Data pipeline

1. **Start with**: Schema/contract validation on inputs and outputs, data-quality assertions (nullability, ranges, uniqueness)
2. **Add next**: Golden datasets (known input → known output) and metamorphic relations (e.g. row count preserved, aggregates consistent)
3. **Add for evolution**: Replay against historical data; diff new vs old pipeline output
4. **Always include**: Lineage tracking and freshness/volume anomaly alerts — failures are silent corruption, not crashes

### Infrastructure/IaC

1. **Start with**: Plan validation (`terraform plan`, CDK diff) and policy-as-code gates (OPA/Conftest, Sentinel, cdk-nag)
2. **Add next**: IaC security scanning (tfsec, checkov, kics, terrascan) in pre-commit and CI
3. **Add for deployment**: Progressive rollout, post-apply health checks, automated rollback
4. **Always include**: Drift detection comparing live state to declared state

### Legacy monolith

1. **Start with**: Approval/characterization tests that freeze current observable behavior of the code you intend to change
2. **Add next**: Golden-trace replay — capture sanitized production traffic, normalize nondeterministic fields, replay against the candidate
3. **Add for refactor safety**: Integration smoke tests and baseline telemetry to detect drift
4. **Always include**: Strangler-edge contract tests as behavior moves out of the monolith
5. **Sequencing note**: freeze behavior *first*; do not begin deep refactors until a characterization net and golden traces are green

### Agent-written

1. **Start with**: Reviewed acceptance criteria and ordinary behavior/boundary gates; respect tool permissions
2. **Where useful**: Separate evaluation cases, accepted/rejected controls, and independent expected values
3. **For operated systems**: Progressive delivery with qualified detection and rollback
4. **Review limits**: Shared oracle errors, repeated holdout exposure, and existing approval requirements
