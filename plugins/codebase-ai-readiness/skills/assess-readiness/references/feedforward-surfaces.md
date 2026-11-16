# Feedforward Surfaces

## Definition

Feedforward controls are mechanisms placed *before* agent action to steer toward correct
output on the first attempt. They reduce iteration count and context window consumption
by preventing errors rather than correcting them after the fact.

## Two forms of feedforward

### Document-based feedforward

Instruction files, specifications, and conventions loaded into context before work begins.

| Surface | What it provides | Where to find it |
|---------|-----------------|------------------|
| Instruction files | Project-scoped rules and conventions | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.cursor/rules/` |
| Architecture docs | Structural constraints, dependency rules | `docs/adr/`, `ARCHITECTURE.md`, `docs/design/` |
| Templates | Structured formats for new code | Issue/PR templates, file generators, `plop`/`hygen` configs |
| Domain models | Shared vocabulary and relationships | `docs/domain/`, glossary files, bounded-context maps |
| Coding standards | Style and convention enforcement | `.editorconfig`, style guides, `CONTRIBUTING.md` |

### Computational feedforward

Tools that run during or immediately after generation, catching structural errors
deterministically and cheaply before they compound.

| Surface | What it prevents | Where to find it |
|---------|-----------------|------------------|
| Type system (strict) | Shape errors, null violations, wrong types | `tsconfig.json` strict, `mypy.ini` strict, `--strict` flags |
| Linter config | Style drift, known antipatterns, banned APIs | `.eslintrc*`, `ruff.toml`, `.golangci.yml`, `clippy.toml` |
| Schema validators | Invalid data shapes at API boundaries | JSON Schema, Zod, Pydantic, protobuf |
| Module boundary linters | Unauthorized cross-module imports | eslint-plugin-boundaries, deptry, madge, ArchUnit |
| Formatters | Layout inconsistencies | Prettier, Black, rustfmt, gofmt |
| Security scanners | Known vulnerability patterns | Semgrep, CodeQL, Snyk, bandit |
| Pre-commit hooks | All of the above, on every change | `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml` |
| Bypass guards | Agents skipping hooks (`git commit --no-verify`) | Agent config denying bypass commands; server-side branch protection + required checks |

## Pass profiles

The denominator for this category is the **Feedforward surfaces** table in
`category-definitions-agent.md`. Decide PASS or FAIL per row with these profiles:

| Signal | PASS when | FAIL when |
|--------|-----------|-----------|
| Instruction files with project rules | >10 actionable, project-specific rules | Missing, generic, or copied from a template |
| Strict type checking | Strict mode on; escape hatches in <5% of files | Not strict, or escape hatches common |
| Module boundary enforcement | A linter or structural test fails the build on a forbidden import | Boundaries only in docs, or absent |
| Pre-commit hooks per-file | Type checker + linter + formatter run on changed files | No hooks, or formatter only |
| Non-bypassable hooks | Agent config denies skip commands such as `--no-verify` | Any agent can bypass locally (server-side gate is scored under CI reliability) |
| Templates and generators | Templates or generators for the common file kinds | Ad-hoc file creation |
| Security scanners pre-commit | A scanner runs on every commit | Only in CI, or none |
| Code-health scanners | Complexity or dead-code checks fail the build | None configured |

## Key principle

> When an agent makes the same mistake twice, treat it as a feedforward gap.

The presence of feedforward surfaces is a leading indicator of codebase AI-readiness.
Their absence means every agent session restarts from zero, repeating the same
discovery and making the same avoidable errors.
