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

## Scoring signals

### Strong feedforward (score 76-100)
- Instruction file with >10 actionable rules specific to the project
- Strict type checking with <5% escape hatches
- Module boundary enforcement via linter or structural tests
- Pre-commit hooks run type checker + linter + formatter on every change
- Hooks are non-bypassable: agent config denies skip commands, CI enforces server-side
- Templates exist for common file types (components, services, tests)
- Architecture docs specify which module depends on what

### Moderate feedforward (score 51-75)
- Instruction file exists but is generic or incomplete
- Type checking enabled but not strict, or with many escape hatches
- Linter configured but only enforces style, not architecture
- Pre-commit hooks exist but only run formatter
- Some templates, but ad-hoc file creation is common

### Weak feedforward (score 26-50)
- No instruction file, but README covers conventions
- Linter exists but runs only in CI (not per-file)
- Types used but not enforced (no strict mode)
- No module boundary enforcement
- No pre-commit hooks

### Absent feedforward (score 0-25)
- No instruction file, no agent context
- No linter or type checking
- No pre-commit hooks
- No templates or conventions documented
- Agents must infer all conventions from code patterns

## Key principle

> When an agent makes the same mistake twice, treat it as a feedforward gap.

The presence of feedforward surfaces is a leading indicator of codebase AI-readiness.
Their absence means every agent session restarts from zero, repeating the same
discovery and making the same avoidable errors.
