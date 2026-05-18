# Detection Patterns

What tools and gate configurations catch each AI smell. Use this to map existing gates to smell categories and recommend missing ones.

## AI001: Plausible Fabrication

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Unused dependency detection | `depcheck`, `deptry`, `go mod tidy` | Imported packages that don't exist or aren't used |
| Type checking | `tsc --noEmit`, `mypy`, `pyright` | Calls to non-existent functions/methods |
| Schema validation | OpenAPI linting, protobuf compilation | API calls to undefined endpoints |
| Lockfile integrity | `npm ci`, `pip install --require-hashes` | References to non-existent package versions |
| Behavioral twin testing | Agent-built service clones, scenario runners | Fabricated API behavior that mocks wouldn't catch |
| Contract tests | Pact, Spring Cloud Contract | Schema drift between services |

**Note:** Interface mocks (`jest.mock`, `unittest.mock`) do NOT catch fabrication — the agent writes both code and mocks, creating a closed plausibility loop. Only external verification (twins, contracts against real schemas) breaks this circularity.

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
| Silent success masking | Custom semgrep: `catch (...) { return [] }`, `catch (...) { return null }` | Catch blocks that return plausible defaults instead of surfacing failure |
| Startup validation enforcement | Custom CI script checking `main`/`index` for config validation | Config validated lazily on first use instead of at startup |
| Default substitution on failure | Custom semgrep: `catch (...) { $X = $DEFAULT }` | Parse/fetch failures masked by default values without logging |
| Boundary validation absence | Architecture rules, custom semgrep | Missing input validation at public API / function entry points |

**Fail-fast principle:** AI-generated code typically handles errors deep in call stacks rather than validating at boundaries. The most dangerous pattern is not an empty catch block (easily spotted) but a catch block that returns something plausible — an empty array that looks like "no results", a null that looks like "not found", a default timeout that happens to work today. These create systems that continue operating with hidden corruption.

**Detection priority for semgrep rules:**
```yaml
# Silent success masking — high priority
- pattern: |
    try { ... }
    catch (...) { return []; }
- pattern: |
    try { ... }
    catch (...) { return null; }
- pattern: |
    try { ... }
    catch (...) { return {}; }
# Default substitution — medium priority
- pattern: |
    try { $RESULT = $EXPR; }
    catch (...) { $RESULT = $DEFAULT; }
```

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
| Magic number linting | eslint `no-magic-numbers`, ruff `PLR2004` | Hard-coded numeric literals without named constants |
| Magic string detection | Custom semgrep, SonarQube string duplication | Repeated string literals (URLs, ports, paths) across files |
| Config scatter detection | Custom grep/semgrep for common patterns | Same value hard-coded in multiple locations (timeouts, size limits, ports) |

**Hard-coding principle:** AI-generated code is particularly prone to inlining values because models lack awareness of project configuration conventions. A value that appears in 3+ files (e.g., upload size limit, retry count, API endpoint) should live in a single config source. Three checks for any literal:
1. Does the value encode domain knowledge? (Should be a named constant)
2. Does the value vary across environments? (Should be in config/env)
3. Does a canonical config home already exist? (Use it consistently)

**Detection patterns for common hard-coded values:**
```bash
# Repeated numeric literals (excluding 0, 1, -1)
grep -rn '[^a-zA-Z_][0-9]\{2,\}' src/ --include="*.ts" --include="*.py"

# Hard-coded ports
grep -rn ':\(3000\|5432\|6379\|8080\|8443\|27017\)' src/

# Hard-coded URLs/hosts
grep -rn 'https\?://[a-z]' src/ --include="*.ts" --include="*.py" | grep -v test | grep -v spec

# Repeated timeout/retry values
grep -rn 'timeout.*[0-9]\{4,\}\|retry.*[0-9]' src/
```

## AI008: Implicit Drift

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Version range linting | Custom semgrep/grep, `npm-package-json-lint` | Floating semver ranges (`^`, `~`, `*`, `>=`) beyond patch |
| Docker tag linting | `hadolint`, custom Dockerfile lint | `FROM image:latest` or untagged base images |
| Lockfile enforcement | `npm ci` (fails without lockfile), `pip install --require-hashes` | Missing or outdated lockfiles |
| Model ID pinning | Custom grep/semgrep | Unpinned model aliases (`gpt-4`, `claude-sonnet`) without dated version |
| Infrastructure pin checks | `tflint`, custom Terraform rules | Unpinned provider/module versions |
| GitHub Action pinning | `actionlint`, `pin-github-action` | Actions referenced by tag instead of SHA |
| Renovate/Dependabot presence | Config file check | No automated update mechanism for pinned versions |

**Pinning principle:** A real pin resolves to the same bytes today, tomorrow, and a year from now. AI-generated code almost always uses the "convenient" form (alias, latest, floating range) because training data shows both pinned and unpinned equally. The harm is silent: code works on generation day but breaks when the mutable reference resolves differently — with zero traceable change in the repo.

**Detection patterns:**
```bash
# Docker: unpinned base images
grep -n 'FROM.*:latest\|FROM [^:]*$' Dockerfile*

# package.json: floating ranges beyond patch
grep -n '"\^[0-9]\|"~[0-9]\|"\*"\|">=\|">[0-9]' package.json

# Python: unpinned in requirements
grep -vn '==\|@' requirements*.txt | grep -v '^#\|^$'

# GitHub Actions: tag references instead of SHA
grep -rn 'uses:.*@v[0-9]\|uses:.*@main\|uses:.*@master' .github/

# Model aliases without version
grep -rn 'model.*=.*["'"'"']\(gpt-4\|claude\|sonnet\|opus\|haiku\|gemini\)["'"'"']' src/ | grep -v '\-[0-9]\{4\}'

# Terraform: unpinned providers/modules (missing exact version constraint)
grep -n 'version\s*=' *.tf | grep -v '"[0-9]\+\.[0-9]\+\.[0-9]\+'
```

**Note:** Pinning without an update mechanism (Dependabot, Renovate, scheduled CI) is incomplete. The assessment should check for both the pin AND the deliberate update process.

## Minimum Viable Gate Set

For teams starting from zero, recommend in priority order:
1. Type checking (catches AI001)
2. Empty catch lint rules + silent success masking (catches AI004)
3. Mutation testing (catches AI005)
4. Duplication detection (catches AI006)
5. Import boundary enforcement + magic value linting (catches AI007)
6. Dead code detection (catches AI002, AI003)
7. Lockfile enforcement + Docker tag linting (catches AI008)
