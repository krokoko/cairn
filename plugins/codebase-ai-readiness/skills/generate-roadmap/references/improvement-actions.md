# Improvement Actions Catalog

## Structure and modularity

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Organize source into feature directories | Medium | +15-25 | Group related files by domain |
| Extract shared utilities; add barrel exports | Medium | +10-15 | Reduces coupling, clarifies public API |
| Add dependency analysis + custom boundary linters to CI | Medium | +10-20 | madge/deptry + mechanical enforcement of layer constraints |
| Isolate agent-writable components (containers, WASM, sandbox) | Medium | +10-20 | Safe iteration without risk to production-critical paths |

## Documentation

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Write or improve README with setup steps | Small | +15-20 | Most impactful single doc action |
| Add ADR directory with first decisions | Small | +10-15 | Template: MADR format |
| Add inline docstrings + CHANGELOG | Medium | +10-15 | Public API docs; commitlint for changelog |

## Testable boundaries

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Add test framework and first test suite | Medium | +20-30 | Foundation for everything else |
| Separate unit and integration tests | Small | +10-15 | Different directories or markers |
| Add test fixtures / factories | Medium | +10-15 | Reduces test setup duplication |
| Add property-based tests for key functions | Medium | +15-20 | Hypothesis, fast-check, proptest |

## CI reliability

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Add CI pipeline with test execution | Medium | +20-30 | GitHub Actions is simplest start |
| Add coverage reporting + required checks | Small | +10-15 | Codecov; branch protection rules |
| Add linting to CI | Small | +5-10 | ESLint, ruff, clippy, golangci-lint |
| Add pre-commit hooks for type checking and linting | Small | +10-15 | Shift checks left; agents catch errors per-file, not per-PR |

## Typing strength

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Enable strict type checking | Small | +15-25 | tsconfig strict, mypy strict |
| Remove type escape hatches | Medium | +10-20 | Eliminate `any`, `type: ignore` |
| Add typed API boundaries | Medium | +10-15 | Request/response types |

## Deterministic environment and deployment

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Add Docker or devcontainer config | Medium | +15-25 | One-command reproducible env |
| Add `.env.example` with all variables | Small | +10-15 | Document required config |
| Add mise.toml or Nix flake for tools | Small | +10-15 | Pin tool versions |
| Add Infrastructure as Code (CDK, Terraform, Pulumi) with CI validation | Large | +20-30 | Codify deployment; agents can review and modify infra |

## Architecture decisions

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Create ADR directory with template | Small | +15-25 | MADR or similar template |
| Add CODEOWNERS file | Small | +10-15 | Maps directories to owners |

## Machine-readable intent

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Add OpenAPI or protobuf for APIs | Medium | +15-25 | Machine-checkable API contracts |
| Add JSON Schema for config files | Small | +10-15 | Validates configuration |
| Add property-based tests + assertion contracts | Medium | +15-20 | Machine-checkable invariants and pre/postconditions |
| Make key modules regenerative (specs+tests define behavior fully) | Large | +10-20 | Components rebuildable from contracts alone; L5 enabler |

## Progressive context disclosure

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Add CLAUDE.md / AGENTS.md at root | Small | +15-25 | Entry point for AI agents |
| Add per-directory READMEs; cross-link docs | Medium | +10-15 | Layered navigation, prevents orphaned docs |
| Add versioned execution plans directory | Small | +10-15 | Active plans, progress logs, decision logs in-repo |

## Hidden state and magic

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Create `.env.example` + config schema validation | Medium | +15-20 | Discoverable config; Zod/Pydantic/JSON Schema enforced |
| Document feature flags in one place | Small | +5-10 | Central registry of toggles |

## Repository-scale reasoning

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Standardize module directory structure | Medium | +10-20 | Same layout everywhere |
| Eliminate term synonyms | Small | +10-15 | One term per concept project-wide |
| Single canonical build/test/deploy command | Small | +5-10 | One way to do each operation |

## Failure mode legibility

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Audit and remove swallowed exceptions | Medium | +15-20 | No empty catch/except blocks |
| Add structured error types or codes | Medium | +10-15 | Error classes, not just strings |
| Write agent-targeted remediation in lint/CI error messages | Small | +10-15 | Errors tell agents what to fix, not just what failed |

## Feedforward surfaces

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Create instruction file (CLAUDE.md/AGENTS.md) with 10+ project rules | Small | +20-30 | Single highest-impact feedforward action for agents |
| Enable strict type checking and reduce escape hatches | Medium | +15-20 | tsconfig strict, mypy strict, eliminate `any`/`type: ignore` |
| Add module boundary linter to prevent unauthorized imports | Medium | +15-20 | eslint-plugin-boundaries, deptry, madge, ArchUnit |
| Add pre-commit hooks running type checker + linter per-file | Small | +15-20 | Catches errors before they compound |
| Add file/component templates for common patterns | Small | +10-15 | plop, hygen, or simple template files |
| Add security scanner to pre-commit (Semgrep, bandit, gitleaks) | Small | +10-15 | Prevents security issues proactively |

## Compound engineering readiness

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Start instruction file and commit to adding rules after each correction | Small | +15-25 | Begin the feedback flywheel |
| Create first custom skill for a repeated workflow | Medium | +10-15 | Package a task agents perform repeatedly |
| Add hooks that enforce recently-discovered conventions | Small | +10-15 | Convert corrections into automated enforcement |
| Add regression tests for each bug found during agent work | Small | +10-15 | Prevents re-introduction; compounds over time |
| Schedule monthly instruction file review for stale/conflicting rules | Small | +5-10 | Maintenance prevents rot |

## Context engineering friendliness

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Split files >500 lines into focused, single-responsibility modules | Medium | +15-25 | Largest impact on agent comprehension |
| Add per-module READMEs with purpose and API summary | Medium | +10-15 | Enables progressive context loading |
| Rename generic files (utils, helpers, common) to domain-specific names | Small | +10-15 | Improves search and retrieval |
| Add explicit module exports (barrel files, `__init__.py`) | Small | +10-15 | Clear public API surface |
| Add ARCHITECTURE.md with system-level structure | Small | +10-15 | Entry point for understanding module relationships |
| Standardize documentation headings for searchability | Small | +5-10 | Structured headings enable targeted retrieval |
