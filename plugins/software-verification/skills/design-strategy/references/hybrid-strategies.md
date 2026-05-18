# Hybrid Verification Strategies

## Archetype-to-stack mapping

| Archetype | Recommended stack | Why this mix works |
|-----------|-------------------|-------------------|
| Deterministic library | Types + unit tests + property tests + fuzzing + sanitizers + selective SMT/deductive | Semantics are local, input-heavy; generative methods dominate |
| CRUD/API service | Contracts/schemas + types + linters + unit/integration/regression + canaries + runtime SLOs | Most failures are interface, config, regression; proofs rarely justify ROI |
| Distributed/stateful | Formal spec + model checking + deterministic replay + integration/system tests + runtime verification + canaries + chaos | Interleavings and partial failures are the hard part |
| Safety/security kernel | Contracts + deductive verification + SMT proofs + abstract interpretation + theorem proving + operational checks | Failure cost justifies proof investment; runtime catches spec mismatches |
| ML-backed | Metamorphic + differential evaluation + statistical thresholds + shadow testing + canaries + human escalation | Exact outputs unavailable; alternative oracles and operational validation dominate |
| Agent-written | Equivalence oracle + held-out validation + sandboxing + progressive delivery + telemetry + risk-based human approval | Mirrors strongest pattern for autonomous iteration |

## Detailed recommendations per archetype

### Deterministic library

1. **Start with**: Strong types, comprehensive unit tests
2. **Add next**: Property-based tests for core invariants (round-trips, associativity, ordering)
3. **Add for native code**: Fuzzing (libFuzzer/AFL) + sanitizers (ASan, UBSan)
4. **For highest assurance**: SMT-backed verification (Kani, Dafny) on critical functions

### CRUD/API service

1. **Start with**: Request/response type schemas, integration tests
2. **Add next**: Contract tests at API boundaries, regression replay from production traces
3. **Add for deployment safety**: Canary analysis, runtime SLO monitoring
4. **For compliance**: Audit logging, required approval gates

### Distributed/stateful

1. **Start with**: Write a formal spec (TLA+ or Alloy) of the protocol
2. **Add next**: Model check the spec (TLC, Apalache, Stateright)
3. **Add for implementation**: Deterministic replay/simulation testing
4. **Add for production**: Runtime monitors for temporal properties, chaos experiments

### Safety/security kernel

1. **Start with**: Explicit contracts (pre/postconditions, invariants)
2. **Add next**: Deductive verification or SMT-backed proof
3. **Add for crypto/compilers**: Interactive theorem proving (Lean, Coq)
4. **Always include**: Operational monitoring as spec-reality check

### ML-backed

1. **Start with**: Metamorphic tests (known input transformations -> expected output relations)
2. **Add next**: Shadow testing against production traffic
3. **Add for deployment**: Statistical monitoring, drift detection, canary analysis
4. **Always include**: Human-in-the-loop for edge cases and low-confidence outputs

### Agent-written

1. **Start with**: Sandbox execution, equivalence oracle (compare output to reference)
2. **Add next**: Held-out validation against known-good examples
3. **Add for deployment**: Progressive delivery with automated rollback
4. **Always include**: Risk-based human approval for high-blast-radius changes
