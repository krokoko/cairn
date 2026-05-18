# Architecture Fitness Functions

## Definition

An architecture fitness function is an automated check that verifies a system continues
to honor specific architectural decisions. It detects structural drift before it becomes
costly — particularly critical in agentic systems where agents may not understand
implicit architectural constraints.

## Why fitness functions matter for autonomous agents

Architectural decisions erode silently under deadline pressure. When agents write code,
they respond reliably to *automated signals* rather than documentation alone. Fitness
functions provide those signals: when an agent violates an architectural constraint,
the function fails, and the agent self-corrects within its steering loop.

Without fitness functions, architectural rules live only in documentation or human
memory. Agents cannot enforce what they cannot check.

## Types of fitness functions

### 1. Dependency constraints

Prevent unauthorized module dependencies (e.g., UI layer cannot import database layer).

| Tool | Language | How it works |
|------|----------|-------------|
| eslint-plugin-boundaries | TypeScript/JS | Define element types and allowed dependency rules |
| deptry | Python | Detect missing, unused, and transitive deps |
| madge | TypeScript/JS | Circular dependency detection |
| ArchUnit | Java/Kotlin | Test architectural rules as unit tests |
| go-arch-lint | Go | Layer and dependency rules for Go packages |
| cargo-deny | Rust | License, ban, and advisory checks |

Example rule: "No file in `src/domain/` may import from `src/infrastructure/`"

### 2. API surface checks

Ensure public interfaces remain backward-compatible or change deliberately.

| Approach | Tools | What it catches |
|----------|-------|-----------------|
| Schema comparison | openapi-diff, buf breaking | Breaking API changes |
| Contract tests | Pact, Spring Cloud Contract | Consumer expectation violations |
| Type surface checks | api-extractor, cargo-public-api | Unintended public API changes |
| Export validation | Custom barrel file checks | Module surface drift |

Example rule: "No breaking change to openapi.yaml without ADR reference in commit"

### 3. Performance budgets

Measurable thresholds that prevent quality erosion.

| Budget type | Tool | Threshold example |
|-------------|------|-------------------|
| Bundle size | bundlesize, size-limit | < 250kb gzipped |
| Page load | Lighthouse CI | LCP < 2.5s |
| Response latency | k6, autocannon thresholds in CI | p99 < 200ms |
| Memory usage | Benchmark harness with assertions | < 512MB peak |
| Build time | CI timing assertions | < 5 minutes |
| Test execution | CI timing assertions | < 3 minutes for unit suite |

Example rule: "Bundle size must not increase by more than 5% without reviewer approval"

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

### 1. Express rules as executable assertions

Fitness functions belong in the build pipeline alongside tests and linters.
They must be automated, deterministic, and fast enough to run on every commit.

### 2. One property per function

Each check verifies one architectural property with a clear, specific error message.
Agents need to know exactly what failed and what to fix.

### 3. Include in agent verification commands

For agents to self-correct, fitness functions must be runnable locally with the same
command agents use for verification. If the check only runs in CI, agents cannot
iterate against it.

### 4. Fail with actionable messages

Bad: "Architecture violation detected"
Good: "File src/api/handler.ts imports from src/infrastructure/db.ts — domain layer
      cannot depend on infrastructure. Move the dependency through a port interface."

## Fitness function maturity levels

| Level | Description | Agent impact |
|-------|-------------|-------------|
| 0 | No fitness functions | Agents freely violate architecture |
| 1 | Manual enforcement (code review) | Agents unaware of constraints |
| 2 | CI-only checks | Agents discover violations after push |
| 3 | Local + CI checks, actionable messages | Agents self-correct within iteration loop |
| 4 | Pre-commit + agent hooks, comprehensive | Violations caught per-file; near-zero drift |

## Recommendations by archetype

| Component archetype | Priority fitness functions |
|--------------------|---------------------------|
| Deterministic library | API surface stability, dependency constraints, performance budget |
| CRUD/API service | Schema compatibility, layer compliance, auth invariants |
| Distributed/stateful | Dependency constraints, protocol compatibility, timeout budgets |
| Safety/security kernel | All security invariants, dependency isolation, no-magic rules |
| ML-backed | Performance envelope, API surface, model version pinning |
| Agent-written | Structural rules, naming conventions, test-to-source ratio |
