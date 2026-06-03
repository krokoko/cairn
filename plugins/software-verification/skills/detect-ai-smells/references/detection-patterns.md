# Detection Patterns

What tools and gate configurations catch each AI smell. Load `detection-patterns-gates.md` for AI005–AI010 and the minimum viable gate set.

## AI001: Plausible Fabrication

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Unused dependency detection | `depcheck`, `deptry`, `go mod tidy` | Imported packages that don't exist or aren't used |
| Type checking | `tsc --noEmit`, `mypy`, `pyright` | Calls to non-existent functions/methods |
| Schema validation | OpenAPI linting, protobuf compilation | API calls to undefined endpoints |
| Lockfile integrity | `npm ci`, `pip install --require-hashes` | References to non-existent package versions |
| Behavioral twin testing | Agent-built service clones, scenario runners | Fabricated API behavior that mocks wouldn't catch |
| Contract tests | Pact, Spring Cloud Contract | Schema drift between services |

**Note:** Interface mocks do NOT catch fabrication — the agent writes both code and mocks. Only external verification (twins, contracts against real schemas) breaks this loop.

## AI002: Cargo-Cult Patterns

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Dead code detection | `knip`, `ts-prune`, `vulture` | Unused interfaces, factories, abstractions |
| Architecture enforcement | `dependency-cruiser`, `deptry` | Unnecessary indirection layers |
| Complexity metrics | SonarQube, Code Climate | Over-engineered modules relative to function |

## AI003: Architecture Astronaut

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| File/module size limits | Custom CI script, `tokei` thresholds | Feature spanning too many files |
| Import depth limits | `eslint-plugin-boundaries`, `import-linter` | Excessive layering |
| Dead code detection | `knip`, `ts-prune` | Abstraction layers with no consumers |
| Vocabulary linting | Custom semgrep/grep rules | "Platform"/"engine" in small-scope repos |

## AI004: Shallow Error Handling

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Empty catch lint rules | eslint `no-empty`, ruff `B001`/`E722`, `errcheck` (Go) | Empty or trivial catch blocks |
| Custom semgrep rules | semgrep `try {...} catch ($E) {}` | Log-and-swallow, context stripping |
| Error propagation enforcement | `exhaustive` (TS), custom clippy | Unhandled error variants |
| Silent success masking | Custom semgrep on catch returning `[]`, `null`, `{}` | Plausible defaults instead of surfacing failure |
| Startup validation enforcement | Custom CI script on `main`/`index` | Config validated lazily instead of at startup |
| Default substitution on failure | Custom semgrep on catch assigning defaults | Parse/fetch failures masked without logging |
| Boundary validation absence | Architecture rules, custom semgrep | Missing input validation at public API entry points |

**Fail-fast principle:** The most dangerous pattern is a catch that returns something plausible — empty array, null, default timeout. These create hidden corruption.

**Detection priority for semgrep rules:**
```yaml
- pattern: |
    try { ... }
    catch (...) { return []; }
- pattern: |
    try { ... }
    catch (...) { return null; }
- pattern: |
    try { ... }
    catch (...) { return {}; }
- pattern: |
    try { $RESULT = $EXPR; }
    catch (...) { $RESULT = $DEFAULT; }
```
