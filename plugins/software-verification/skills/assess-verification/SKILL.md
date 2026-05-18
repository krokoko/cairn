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

Assess the current verification maturity of a codebase. Produce a `verification-report.md` with maturity tier, component breakdown, missing oracles, exactness analysis, human review requirements, and autonomy candidates.

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
| Replay/held-out data | Historical inputs with known-good outputs |
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

### Step 8: Write the report

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
```
