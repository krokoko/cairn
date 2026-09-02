# Verification Maturity Model

## Maturity tiers

| Tier | Name | Description | Key indicators |
|------|------|-------------|----------------|
| 0 | None | No automated verification | No test files, no CI, no linting |
| 1 | Basic | Tests exist but may be unreliable | Test files present, may not run in CI, possibly flaky |
| 2 | Reliable | Consistent test suite with CI gating | CI runs tests on every PR, required checks, low flake rate |
| 3 | Generative | Broad input exploration + explicit contracts | Property tests or fuzzing, schemas/contracts at boundaries |
| 4 | Formal + Operational | Proofs for critical paths, runtime validation | Model checking or deductive proofs, shadow/canary deployment |
| 5 | Evidence pipeline | Full verification loop with automated promotion | Structured evidence, replay labels, spec↔impl conformance, spec continuity design→CI→runtime |

## Tier assessment criteria

### Tier 0 indicators
- No `test/`, `tests/`, or `*_test.*` files
- No CI configuration
- No linting or type checking configured

### Tier 1 indicators
- Test files exist (any count)
- Test framework configured (jest.config, pytest.ini, etc.)
- Tests may not run in CI or may be frequently skipped

### Tier 2 indicators
- CI pipeline runs tests on every PR
- Required checks block merge on failure
- Flake rate < 5%
- Coverage is measured (not necessarily enforced)

### Tier 3 indicators
- Property-based tests exist (Hypothesis, fast-check, proptest)
- OR fuzzing harness exists with meaningful coverage
- Schemas or contracts enforce interface correctness
- Type checking in strict mode

### Tier 4 indicators
- Formal specification exists for at least one critical component
- Model checking or bounded verification has been applied
- *Recommended, not required:* model↔implementation conformance testing (Quint Connect, P test drivers) — its absence is the usual Tier 4→5 gap
- Runtime verification or production monitors check invariants
- Shadow testing or canary analysis used for deployments
- Oracle integrity assessed — sound oracles on critical paths (`../../design-strategy/references/oracle-integrity.md`)

### Tier 5 indicators
- All critical paths have machine-checkable specifications
- **Model↔implementation conformance** on every critical path with a formal model, and the **same behavioral specification** used at design, CI, and runtime where applicable (P/Quint/PObserve continuity)
- Verification evidence is structured and feeds deployment decisions
- Replay labels capture historical behavior for regression
- Automated promotion/rollback based on evidence thresholds
- Verifier-guided search **prerequisites** in place: server-side authoritative verifier, approved spec/holdouts outside agent write scope, CI separates required checks from informational metrics (`../../design-strategy/references/verifier-guided-search.md`; search strategy itself is a harness choice, recommended in design-strategy)
- Human review is exception-based, not routine-based
- All critical-path oracles rated **sound** integrity (not agent-mutable)

## Agentic test pyramid

For agent-driven codebases, organize tests by **uncertainty tolerance** not just type:

| Layer | What belongs | Speed | Reliability |
|-------|-------------|-------|-------------|
| Base (most tests) | Deterministic tests on non-LLM components: validators, state machines, tool handlers | ms | High |
| Middle | Recorded tool interactions + LLM-as-judge evaluations against rubrics | seconds | Medium |
| Top (fewest tests) | Live staging simulations, agentic QA charters, human spot-checks | minutes | Variable |

Push determinism as low as possible — base-layer tests are cheap, fast, and trustworthy.

## Mapping to autonomy levels

| Verification tier | Enables autonomy level | Rationale |
|-------------------|----------------------|-----------|
| 0 | L0 | No safety net for agent actions |
| 1 | L1 | Agents can suggest; humans must verify |
| 2 | L2 | Agents can act; CI catches regressions; human reviews |
| 3 | L3 | Agents iterate within typed, tested, contracted bounds |
| 4 | L4 | Automated checks are authoritative; agents are gated; oracle integrity required |
| 5 | L5 | Full evidence loop; verifier-guided search prerequisites; sound non-mutable oracles |

**L5 hard gate:** Agent-mutable oracles, LLM-as-final-authority, or combined-score candidate
selection without mandatory tier → not L5-ready regardless of other indicators.
