# Category Definitions

Load `category-definitions-agent.md` for feedforward, compound engineering, and context engineering.

## Categories

### Structure and modularity
| Signal | Where to check |
|--------|----------------|
| Clear directory hierarchy | Top-level `ls`, nesting depth |
| Module boundaries | Separate packages, `exports`, `__init__.py`, `mod.rs` |
| Naming consistency | File and directory naming patterns |
| Separation of concerns | Routes vs logic vs data in distinct directories |
| Architectural isolation | WASM, sandboxed containers, process separation, stable/experimental split |
| Mechanically-enforced boundaries | Custom linters, structural tests, or dependency-direction checks in CI |

### Documentation
| Signal | Where to check |
|--------|----------------|
| README with setup instructions | Root README.md |
| API docs + ADRs | `docs/api/`, docstrings, `docs/adr/`, `docs/decisions/` |
| Changelog | `CHANGELOG.md`, conventional commits config |

### Testable boundaries
| Signal | Where to check |
|--------|----------------|
| Test directories exist | `test/`, `tests/`, `__tests__/`, `*_test.*`, `*_spec.*` |
| Test-to-source ratio | Count test files vs source files (>0.5 is good) |
| Integration test separation | Separate directories or markers for integration tests |
| DI / interfaces | Constructor injection, interface types, trait objects |

### CI reliability
| Signal | Where to check |
|--------|----------------|
| CI config exists | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` |
| Multiple checks + coverage | Count jobs/steps; `codecov.yml`, branch protection rules |
| Flakiness signals | `retry:`, `flaky` annotations, timeout overrides |
| Shift-left checks | `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`, watch mode configs |
| Test impact analysis | pytest-testmon, Jest `--onlyChanged`, Launchable — run only affected tests (essential at agent test volume) |

### Typing strength
| Signal | Where to check |
|--------|----------------|
| Type annotations + strict mode | `tsconfig.json` strict, `mypy.ini` strict |
| Escape hatches | Count of `any`, `type: ignore`, `as unknown`, `unsafe` |
| Typed boundaries | Request/response types, API contracts typed |

### Deterministic environment and deployment
| Signal | Where to check |
|--------|----------------|
| Container / reproducible env | `Dockerfile`, `.devcontainer/`, `flake.nix`, `mise.toml` |
| Env template | `.env.example`, `.env.template` |
| Setup script | `Makefile`, `just`, `mise run setup`, documented one-liner |
| Infrastructure as Code | `cdk.json`, `*.tf`, `Pulumi.yaml`, `template.yaml` (SAM), `*.bicep` |
| Deployment codified | IaC in version control, not manually provisioned (no click-ops) |
| IaC tested | `cdk synth`, `terraform plan` in CI, infrastructure unit tests |

### Architecture decisions
| Signal | Where to check |
|--------|----------------|
| ADR directory | `docs/adr/`, `docs/decisions/`, `ADR/` |
| CODEOWNERS | `.github/CODEOWNERS`, `CODEOWNERS` |
| Design docs | `docs/design/`, `docs/rfcs/`, `DESIGN.md` |
| Enforced decisions | A documented decision is traceable to the mechanical check that enforces it — ADR references its fitness function/lint rule, or the check cites the ADR (the *decision→enforcement* link; the generic boundary check itself is scored under Structure and modularity) |
| Living decisions | ADRs carry Status (Accepted/Superseded) and dates; superseded decisions are linked, not deleted — guards against decision rot |

### Machine-readable intent
| Signal | Where to check |
|--------|----------------|
| API + data schemas | `openapi.*`, `*.graphql`, `*.proto`, `*.schema.json`, Zod/Pydantic |
| Contracts / property tests | Assertions, invariants, Hypothesis, fast-check |
| Formal specs | `*.tla`, `*.als` (Alloy), `*.dfy` (Dafny) |
| Executable acceptance criteria | Gherkin `.feature` files; BDD step defs (Cucumber, Behave, SpecFlow) |
| Requirement traceability | PRs link issues (`Closes #`); tests tag requirement IDs; requirement-coverage report |
| Regenerative readiness | Components definable by specs+tests alone; can be deleted and rebuilt |

### Progressive context disclosure
| Signal | Where to check |
|--------|----------------|
| Agent context file | `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/` |
| Layered docs | Root README links to deeper docs; per-folder READMEs |
| Cross-linking + entry point | Docs reference each other; README states what/how/where next |
| Plans as versioned artifacts | `docs/plans/`, `docs/exec-plans/`, active/completed plans in-repo |
| Decisions linked from agent context | `AGENTS.md`/`CLAUDE.md` references the decision corpus (ADRs, specs, `.feature` files) so an agent discovers constraints, not just file locations |

### Hidden state and magic
| Signal | Where to check |
|--------|----------------|
| Env vars documented | `.env.example`, `.env.template`, config reference doc |
| Config schemas | `config.schema.json`, Zod/Pydantic config validation |
| No implicit defaults | Grep for env lookups without fallback docs |
| Feature flags / magic visible | Flags in one place; middleware/decorators documented |

### Repository-scale reasoning
| Signal | Where to check |
|--------|----------------|
| Consistent naming | Same concept uses same term across all modules |
| No synonyms | Check for handler/processor/manager doing the same role |
| Predictable patterns | Each module follows same directory structure |
| One canonical way | Single build/test/deploy command, not multiple alternatives |
