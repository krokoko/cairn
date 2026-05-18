---
name: assess-verification
description: |
  Assess the current verification maturity of a codebase and identify gaps.
  Trigger phrases: "assess verification", "verification maturity",
  "how is my testing", "verification strategy assessment",
  "what is my verification coverage", "audit my tests"
argument-hint: "[path-to-codebase] (defaults to current directory)"
allowed-tools: Read Bash Glob Grep
user-invocable: true
---

# Software Verification Assessment

Assess the current verification maturity of a codebase. Produce a `verification-report.md` with maturity tier, component breakdown, missing oracles, exactness analysis, human review requirements, autonomy candidates, feedback loop completeness, workflow gate assessment, and shift-left positioning.

## Workflow

### Step 1: Inventory existing verification

Search for all verification-related artifacts:

**Testing:**
- Test files: `*_test.*`, `*_spec.*`, `test_*.*`, `tests/`, `__tests__/`
- Test config: `jest.config.*`, `pytest.ini`, `pyproject.toml [tool.pytest]`, `vitest.config.*`
- Property tests: imports of `hypothesis`, `fast-check`, `proptest`, `QuickCheck`
- Fuzzing: `fuzz/`, `*_fuzz_test.go`, `cargo-fuzz` config, `AFL` configs
- Mutation testing: `mutmut`, `stryker.conf.*`, `cargo-mutants` config

**Static analysis:**
- Linters: `.eslintrc*`, `ruff.toml`, `.golangci.yml`, `clippy.toml`
- Type checkers: `tsconfig.json`, `mypy.ini`, `pyrightconfig.json`
- SAST tools: `.semgrep/`, `codeql-config.yml`
- Sanitizers: ASan/TSan/UBSan flags in build configs or CI
- Profiling: `pprof`, `perf`, `py-spy` configurations or scripts

**Contracts and schemas:**
- Schemas: `*.schema.json`, `*.proto`, `openapi.*`, `*.graphql`
- Contracts: assertions, `icontract`, `contracts` library imports, `invariant`
- Consumer-driven contracts: `pact/`, `pacts/`, Pact broker config, Spring Cloud Contract stubs
- Formal specs: `*.tla`, `*.cfg` (TLC), `*.als`, `*.dfy`

**CI and operational:**
- CI config: `.github/workflows/`, `.gitlab-ci.yml`
- Coverage: `codecov.yml`, coverage report configs
- Canary/shadow: feature flag configs, deployment configs, traffic splitting

### Step 2: Classify components

Identify distinct components or modules. For each, determine:

Load `references/decision-framework.md` for classification guidance. Load `references/method-failure-modes.md` to understand risks of current methods and gaps in assurance.

| Property | Options |
|----------|---------|
| **Archetype** | Deterministic library, CRUD/API service, Distributed/stateful, Safety/security kernel, ML-backed, Agent-written |
| **Criticality** | High (safety, security, money, core data), Medium (business logic), Low (UI, utilities) |
| **Determinism** | Deterministic, Concurrent/distributed, Probabilistic/learned |
| **Current verification** | List which methods are already applied |

### Step 3: Score verification maturity

Load `references/maturity-model.md` and assign a tier (0-5):

- **Tier 0**: No automated verification
- **Tier 1**: Basic tests exist, may be unreliable
- **Tier 2**: Reliable test suite with CI gating
- **Tier 3**: Generative testing + contracts/schemas
- **Tier 4**: Formal methods for critical paths + operational validation
- **Tier 5**: Evidence pipeline with replay, shadow, canary, automated promotion

Score both the overall codebase and each individual component.

### Step 4: Identify missing oracles

For each component, answer: "Can we determine if the output is correct?"

Load `references/verification-taxonomy.md` for oracle types.

| Oracle type | When applicable |
|-------------|----------------|
| Exact expected output | Deterministic, well-specified inputs/outputs |
| Metamorphic relations | Output hard to predict but transformations have known effects |
| Differential oracle | Multiple implementations or versions to compare |
| Statistical threshold | Stochastic outputs with bounded distributions |
| Performance envelope | Measurable load/latency/resource bounds that must hold |
| Replay/held-out data | Historical inputs with known-good outputs |
| LLM-as-Judge | Non-deterministic output where human review is too slow/costly |
| Human judgment | Ambiguous outputs requiring domain expertise |

Flag components with **no oracle at all** as critical gaps.

### Step 5: Classify correctness feasibility

For each component, determine:

- **Exact correctness possible**: Deterministic, well-specified, finite inputs — amenable to proof or exhaustive testing
- **Statistical/empirical only**: Learned, stochastic, environment-dependent — requires approximation
- **Mixed**: Core logic is deterministic (provable) but integration is non-deterministic (empirical)

### Step 6: Determine human review requirements

Components that require human review:
- No automated oracle exists
- High blast radius (affects users, data, money)
- Ambiguous requirements (underspecified intent)
- Security/compliance boundaries
- Novel code with no regression baseline

### Step 7: Identify autonomy candidates

Components where AI agents could iterate autonomously:
- Strong test coverage with reliable CI gating
- Type-checked boundaries preventing interface errors
- Property tests or contracts covering key invariants
- Low blast radius or easy rollback
- Clear, well-scoped responsibilities

### Step 8: Assess feedback loop completeness

Evaluate whether verification outputs can be consumed by agents for self-correction.

Load `references/feedback-loop-model.md` for maturity levels and assessment criteria.

Search for indicators:
- **Structured output formats**: JUnit XML generation, SARIF reports, JSON test summaries, coverage in lcov/cobertura
- **CI artifact storage**: Upload steps in CI config (actions/upload-artifact, artifacts: paths)
- **API accessibility**: GitHub Checks API usage, status check webhooks, CI notification configs
- **Agent re-execution triggers**: Workflow dispatch events, retry-on-failure configs, bot-triggered re-runs
- **Failure attribution**: Error formatters that include file paths and line numbers, PR annotations
- **Agent-accessible observability**: Local observability stack (Loki, Prometheus, Tempo, Vector), queryable logs/metrics/traces, per-worktree app isolation

For each verification method found in Step 1, classify its feedback loop level (0-3):

| Method | Output format | Routable? | Feedback loop level |
|--------|--------------|-----------|---------------------|
| ... | ... | ... | ... |

Flag methods at Level 0-1 as gaps: verification exists but agents cannot act on its results.

### Step 9: Assess workflow gate placement

Identify all human review and approval checkpoints in the development workflow:

- **PR review requirements**: Branch protection rules, CODEOWNERS, required approvals count
- **Deployment gates**: Manual approval steps in CI/CD, environment protection rules
- **Change advisory**: CAB processes, architecture review boards referenced in docs
- **Compliance gates**: Security review requirements, audit sign-offs

For each gate, evaluate:

| Gate | Risk class served | Rejection rate (if estimable) | Could agent pre-review replace? | Produces actionable feedback? |
|------|-------------------|-------------------------------|-------------------------------|-------------------------------|
| ... | ... | ... | ... | ... |

Identify:
- **Bottleneck gates**: Required human review on low-risk changes where CI is authoritative
- **Missing gates**: High-risk components with no human checkpoint
- **Duplicate gates**: Same validation done by both CI and human reviewer

### Step 10: Assess shift-left positioning

Evaluate whether checks run at the earliest possible point in the development loop.

Load `references/shift-left-model.md` for the tier model and indicators.

Search for shift-left indicators:
- **Pre-commit hooks**: `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`, `.git/hooks/`
- **Post-tool-use hooks**: Agent hook configs running checks after each file write
- **Watch mode / focused tests**: `jest --watch`, `vitest`, `cargo-watch`, scripts for changed-files-only test runs
- **Editor-time checks**: LSP config, IDE settings running type checker on save

For each verification method found in Step 1, classify its current execution tier (T1-T4):

| Check | Current tier | Ideal tier | Shift-left gap? |
|-------|-------------|-----------|-----------------|
| ... | ... | ... | ... |

Flag checks that run only at T3-T4 but could run at T1-T2 (e.g., type checking only in CI, no pre-commit hooks, no focused test mode).

### Step 11: Write the report

Write `verification-report.md`:

```markdown
# Software Verification Report

## Verification Maturity

**Overall tier**: X/5 — [Tier Name]

## Component Breakdown

| Component | Archetype | Criticality | Current methods | Maturity tier |
|-----------|-----------|-------------|-----------------|---------------|
| ... | ... | ... | ... | ... |

## Missing Oracles

| Component | Current oracle | Gap | Recommended oracle type |
|-----------|---------------|-----|------------------------|
| ... | ... | ... | ... |

## Exactness Analysis

| Component | Feasibility | Rationale |
|-----------|-------------|-----------|
| ... | Exact / Statistical / Mixed | ... |

## Human Review Requirements

| Component | Reason | Review type |
|-----------|--------|-------------|
| ... | ... | ... |

## Autonomy Candidates

| Component | Readiness | Confidence | Remaining gaps |
|-----------|-----------|------------|----------------|
| ... | Ready / Near-ready / Not ready | H/M/L | ... |

## Feedback Loop Completeness

**Overall level**: X/3 — [Level Name]

| Verification method | Output format | Routable to agents? | Level | Gap |
|---------------------|--------------|---------------------|-------|-----|
| ... | ... | ... | ... | ... |

## Workflow Gate Assessment

| Gate | Risk class | Throughput concern? | Recommendation |
|------|-----------|---------------------|----------------|
| ... | ... | ... | Keep / Automate / Remove / Add |

**Bottleneck gates**: ...
**Missing gates**: ...

## Shift-Left Assessment

| Check | Current tier | Ideal tier | Gap | Recommendation |
|-------|-------------|-----------|-----|----------------|
| ... | ... | ... | ... | ... |

**Checks running too late**: ...
```
