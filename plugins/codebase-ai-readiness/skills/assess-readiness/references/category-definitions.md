# Category Definitions

## What to look for in each category

### Structure and modularity
| Signal | Where to check |
|--------|----------------|
| Clear directory hierarchy | Top-level `ls`, nesting depth |
| Module boundaries | Separate packages, `exports`, `__init__.py`, `mod.rs` |
| Naming consistency | File and directory naming patterns |
| Separation of concerns | Routes vs logic vs data in distinct directories |

### Documentation
| Signal | Where to check |
|--------|----------------|
| README with setup instructions | Root README.md |
| API documentation | `docs/api/`, generated docs config, docstrings |
| ADRs | `docs/adr/`, `ADR/`, `docs/decisions/` |
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
| Multiple checks | Count distinct jobs/steps |
| Coverage + required checks | `codecov.yml`, branch protection rules |
| Flakiness signals | `retry:`, `flaky` annotations, timeout overrides |

### Typing strength
| Signal | Where to check |
|--------|----------------|
| Type annotations + strict mode | `tsconfig.json` strict, `mypy.ini` strict |
| Escape hatches | Count of `any`, `type: ignore`, `as unknown`, `unsafe` |
| Typed boundaries | Request/response types, API contracts typed |

### Deterministic local setup
| Signal | Where to check |
|--------|----------------|
| Container / reproducible env | `Dockerfile`, `.devcontainer/`, `flake.nix`, `mise.toml` |
| Env template | `.env.example`, `.env.template` |
| Setup script | `Makefile`, `just`, `mise run setup`, documented one-liner |

### Architecture decisions
| Signal | Where to check |
|--------|----------------|
| ADR directory | `docs/adr/`, `docs/decisions/`, `ADR/` |
| CODEOWNERS | `.github/CODEOWNERS`, `CODEOWNERS` |
| Design docs | `docs/design/`, `docs/rfcs/`, `DESIGN.md` |

### Machine-readable intent
| Signal | Where to check |
|--------|----------------|
| API schemas | `openapi.*`, `swagger.*`, `*.graphql`, `*.proto` |
| Data schemas | `*.schema.json`, Zod/Pydantic models |
| Contracts / property tests | Assertions, invariants, Hypothesis, fast-check |
| Formal specs | `*.tla`, `*.als` (Alloy), `*.dfy` (Dafny) |

### Progressive context disclosure
| Signal | Where to check |
|--------|----------------|
| Agent context file | `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/` |
| Layered docs | Root README links to deeper docs; per-folder READMEs |
| Cross-linking | Documents reference each other (not orphaned) |
| Entry point clarity | README states what it does, how to run, where to go next |

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

### Failure mode legibility
| Signal | Where to check |
|--------|----------------|
| No swallowed exceptions | Grep for empty `catch`, `except: pass`, `|| true` |
| Structured errors | Error classes or codes, not just string messages |
| Fail-fast patterns | Validation at boundaries, early returns on bad input |
| Actionable logging | Error messages say what to do; structured logs with levels |
