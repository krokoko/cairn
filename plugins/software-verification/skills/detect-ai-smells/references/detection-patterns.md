# Detection Patterns

What tools and gate configurations catch each AI smell. Use this to map existing gates to smell categories and recommend missing ones.

## AI001: Plausible Fabrication

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Unused dependency detection | `depcheck`, `deptry`, `go mod tidy` | Imported packages that don't exist or aren't used |
| Type checking | `tsc --noEmit`, `mypy`, `pyright` | Calls to non-existent functions/methods |
| Schema validation | OpenAPI linting, protobuf compilation | API calls to undefined endpoints |
| Lockfile integrity | `npm ci`, `pip install --require-hashes` | References to non-existent package versions |

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

## AI005: Tests Mirroring Implementation

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Mutation testing | `stryker`, `mutmut`, `cargo-mutants` | Tests that pass regardless of code changes |
| Coverage quality metrics | Mutation score vs line coverage | High coverage but low mutation kill rate |
| Test naming conventions | Custom lint rules | Tests describing "how" instead of "what" |

## AI006: Symmetry Without Substance

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Duplication detection | `jscpd`, `cpd`, `dupfinder`, SonarQube | Copy-paste code blocks |
| DRY metric enforcement | Code Climate, custom thresholds | Repeated structures that should be abstracted |

## AI007: Local Reasoning Violations

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Import boundary enforcement | `eslint-plugin-boundaries`, `dependency-cruiser` | Cross-module coupling |
| Complexity limits | Cognitive complexity (SonarQube), cyclomatic | Functions doing too much |
| Global state linting | `no-restricted-globals`, custom rules | Singleton/global access patterns |
| Module fan-in/fan-out | `dependency-cruiser` metrics | Excessive coupling |

## Minimum Viable Gate Set

For teams starting from zero, recommend in priority order:
1. Type checking (catches AI001)
2. Empty catch lint rules (catches AI004)
3. Mutation testing (catches AI005)
4. Duplication detection (catches AI006)
5. Import boundary enforcement (catches AI007)
6. Dead code detection (catches AI002, AI003)
