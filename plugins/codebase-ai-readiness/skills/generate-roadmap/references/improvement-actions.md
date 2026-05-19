# Improvement Actions Catalog

Load `improvement-actions-agent.md` for feedforward, compound engineering, and context engineering.

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
