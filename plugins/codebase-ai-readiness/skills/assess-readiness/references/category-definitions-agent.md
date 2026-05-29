# Category Definitions (Agent Surfaces)

Continues `category-definitions.md`. Agent workflow and failure-legibility categories.

### Failure mode legibility
| Signal | Where to check |
|--------|----------------|
| No swallowed exceptions | Grep for empty `catch`, `except: pass`, `|| true` |
| Structured errors | Error classes or codes, not just string messages |
| Fail-fast patterns | Validation at boundaries, early returns on bad input |
| Agent-targeted remediation | Lint/CI errors include fix instructions, not just failure names |

### Feedforward surfaces

| Signal | Where to check |
|--------|----------------|
| Instruction files with project rules | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.cursor/rules/` — count of actionable rules |
| Strict type checking | `tsconfig.json` strict, `mypy.ini` strict — escape hatch count |
| Module boundary enforcement | eslint-plugin-boundaries, deptry, madge, ArchUnit, structural tests |
| Pre-commit hooks per-file | `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml` — what they run |
| Non-bypassable hooks | Agent config denies `git commit --no-verify` etc.; branch protection requires checks server-side |
| Templates and generators | `plop`, `hygen`, cookiecutter, file templates for common patterns |
| Security scanners pre-commit | Semgrep, bandit, gitleaks, detect-secrets in pre-commit config |

### Compound engineering readiness

| Signal | Where to check |
|--------|----------------|
| Instruction file with iterative growth | `CLAUDE.md`, `AGENTS.md` — rule count, last modified date |
| Custom skills or workflows | `.claude/skills/`, agent skill directories, workflow configs |
| Workflow artifacts (feature context) | `docs/requirements/`, `docs/specs/`, `docs/design/`, `docs/plans/`, `docs/exec-plans/`, `docs/reviews/`, `docs/learnings/` — file count and recency |
| Hooks enforce past corrections | Pre-commit/post-tool hooks beyond basic formatting |
| Regression tests from past bugs | Test commit messages referencing issues; bug-driven test patterns |
| Evidence of maintenance | Recent instruction file updates; hook configs matching current tooling |
| Collaboration measurement enablers | PR templates, agent labels, documented review rubric — see `collaboration-metrics.md` |

### Context engineering friendliness

| Signal | Where to check |
|--------|----------------|
| File size distribution | Average and max lines per file; files >500 lines count |
| Layered documentation | Root README -> ARCHITECTURE -> module READMEs -> inline docs |
| Clear entry points | `main.*`, `index.*`, `app.*`; explicit module exports |
| Retrieval-friendly naming | No generic names (utils, helpers, misc); consistent term usage |
| Structured headings | Markdown docs with clear hierarchy; searchable patterns |
