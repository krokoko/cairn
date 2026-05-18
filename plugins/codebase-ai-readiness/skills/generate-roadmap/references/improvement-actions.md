# Improvement Actions Catalog

## Structure and modularity

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Organize source into feature directories | Medium | +15-25 | Group related files by domain |
| Extract shared utilities into a package | Medium | +10-15 | Reduces coupling |
| Add barrel exports / `__init__.py` | Small | +5-10 | Clarifies public API |
| Add a dependency analysis tool to CI | Small | +5-10 | madge, deptry, cargo-deny |
## Documentation

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Write or improve README with setup steps | Small | +15-20 | Most impactful single doc action |
| Add ADR directory with first decisions | Small | +10-15 | Template: MADR format |
| Add inline docstrings to public APIs | Medium | +10-15 | Focus on exported interfaces |
| Add CHANGELOG or conventional commits | Small | +5-10 | Use commitlint or similar |
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
| Add coverage reporting | Small | +10-15 | Codecov, coveralls, or built-in |
| Enable required checks on main branch | Small | +10-15 | Branch protection rules |
| Add linting to CI | Small | +5-10 | ESLint, ruff, clippy, golangci-lint |

## Typing strength

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Enable strict type checking | Small | +15-25 | tsconfig strict, mypy strict |
| Remove type escape hatches | Medium | +10-20 | Eliminate `any`, `type: ignore` |
| Add typed API boundaries | Medium | +10-15 | Request/response types |

## Deterministic local setup

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Add Docker or devcontainer config | Medium | +15-25 | One-command reproducible env |
| Add `.env.example` with all variables | Small | +10-15 | Document required config |
| Add mise.toml or Nix flake for tools | Small | +10-15 | Pin tool versions |

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
| Add property-based tests | Medium | +15-20 | Machine-checkable invariants |
| Add assertion contracts in code | Small | +5-10 | Pre/postcondition checks |

## Progressive context disclosure

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Add CLAUDE.md / AGENTS.md at root | Small | +15-25 | Entry point for AI agents |
| Add per-directory READMEs for complex areas | Medium | +10-15 | Layered navigation |
| Cross-link docs (root links to deeper) | Small | +5-10 | Prevents orphaned docs |

## Hidden state and magic

| Action | Effort | Impact | Notes |
|--------|--------|--------|-------|
| Create `.env.example` documenting all vars | Small | +15-20 | Makes config discoverable |
| Add config schema validation | Medium | +10-15 | Zod, Pydantic, JSON Schema |
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
| Add fail-fast validation at boundaries | Small | +5-10 | Early returns on bad input |
