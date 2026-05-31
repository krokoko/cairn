# Fitness Functions (Implementation)

Continues `fitness-functions.md`. Structural and security rules, implementation principles, and maturity guidance.

### 4. Structural rules

Organization checks that enforce codebase consistency.

| Rule type | Implementation | Example |
|-----------|---------------|---------|
| File-to-test mapping | Custom script or CI check | Every file in `src/` has corresponding test |
| Naming conventions | Custom linter rule | All repository service files end in `.repository.ts` |
| Layer compliance | ArchUnit, custom lint | Domain models have no framework imports |
| Single responsibility | File length + export count checks | No file exports more than 5 public symbols |
| Documentation coverage | Custom check | Every exported function has JSDoc/docstring |

### 5. Security invariants

Automated checks for security-critical properties.

| Invariant | Tool | Example |
|-----------|------|---------|
| No secrets in code | gitleaks, detect-secrets | Pre-commit and CI check |
| Dependency vulnerabilities | Dependabot, Snyk, govulncheck | Block merge on high/critical CVEs |
| Input validation | Semgrep rules, CodeQL | All external inputs validated at boundary |
| Auth checks present | Custom Semgrep rules | Every API endpoint has auth middleware |

## Implementation principles

1. **Executable assertions** — Run in the build pipeline; automated, deterministic, fast.
2. **One property per function** — Clear, specific error messages for agents.
3. **Include in agent verification commands** — Same command locally and in CI.
4. **Actionable failures** — e.g. "domain layer cannot depend on infrastructure" not "architecture violation".

## Fitness function maturity levels

| Level | Description | Agent impact |
|-------|-------------|-------------|
| 0 | No fitness functions | Agents freely violate architecture |
| 1 | Manual enforcement (code review) | Agents unaware of constraints |
| 2 | CI-only checks | Agents discover violations after push |
| 3 | Local + CI checks, actionable messages | Agents self-correct within iteration loop |
| 4 | Pre-commit + agent hooks, comprehensive | Violations caught per-file; near-zero drift |

## Calibration and execution cost

Fitness functions enforce architectural decisions that have *already been made* — they do not make
architectural judgments. Use them to hold a line a human or ADR has drawn, not to discover where the
line should be.

**Calibration tension** — a rule too strict blocks legitimate changes (and agents tend to route
around a hard blocker rather than rethink the change); too loose lets drift through unnoticed. Start
permissive and tighten on observed violations rather than front-loading speculative rules. Each rule
needs ongoing maintenance as the architecture evolves; a stale rule is its own form of drift.

**Execution cost** — keep per-commit fitness functions fast (seconds). Functions that take minutes
(full Lighthouse runs, large benchmark harnesses, deep dependency scans) belong in nightly or
scheduled builds, not the per-commit path, so they do not slow the agent's fast feedback loop. Match
placement to cost: fast structural checks at pre-commit/per-commit; slow envelope checks nightly.

## Recommendations by archetype

| Component archetype | Priority fitness functions |
|--------------------|---------------------------|
| Deterministic library | API surface stability, dependency constraints, performance budget |
| CRUD/API service | Schema compatibility, layer compliance, auth invariants |
| Distributed/stateful | Dependency constraints, protocol compatibility, timeout budgets |
| Safety/security kernel | All security invariants, dependency isolation, no-magic rules |
| ML-backed | Performance envelope, API surface, model version pinning |
| Data pipeline | Schema compatibility, data-quality thresholds, freshness/volume bounds |
| Infrastructure/IaC | Policy-as-code rules, no-secrets, drift detection, blast-radius limits |
| Agent-written | Structural rules, naming conventions, test-to-source ratio |
