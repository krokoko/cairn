# Architecture Fitness Functions

Load `fitness-functions-implementation.md` for structural/security rules, principles, and maturity levels.

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

## Types of fitness functions

### 1. Dependency constraints

Prevent unauthorized module dependencies (e.g., UI layer cannot import database layer).

| Tool | Language | How it works |
|------|----------|-------------|
| eslint-plugin-boundaries | TypeScript/JS | Define element types and allowed dependency rules |
| Import Linter | Python | Enforce forbidden imports and dependency-layer contracts |
| madge | TypeScript/JS | Circular dependency detection |
| ArchUnit | Java/Kotlin | Test architectural rules as unit tests |
| go-arch-lint | Go | Layer and dependency rules for Go packages |
| Custom dependency checks | Rust | Check declared module/crate boundaries within supported analysis scope |

Example rule: "No file in `src/domain/` may import from `src/infrastructure/`"

Keep dependency hygiene separate: deptry finds missing/unused/transitive package dependencies;
cargo-deny checks licenses, bans, and advisories. These do not establish arbitrary module boundaries.

Qualify analyzers with allowed and forbidden fixtures for the actual stack. Include direct, nested,
and indirect imports where supported; record parser versions, source exclusions, unresolved edges,
and exceptions. A clean report supports only the configured rule over the analyzed graph.

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

## Validate maintainability

Separate rule conformance, diagnostic measurements, and maintenance outcomes. Complexity, duplication,
coverage, hotspots, and change coupling identify possible friction; none establishes ease of change.
Try a representative task such as adding an adapter through documented extension points. Record
effort, unexpected edits, regressions, and boundary behavior; interpret findings within that task's scope.
