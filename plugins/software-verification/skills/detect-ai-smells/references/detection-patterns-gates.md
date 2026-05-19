# Detection Patterns (Gates II)

Continues `detection-patterns.md`. Smell categories AI005–AI008 and minimum viable gate set.

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
| Magic string detection | Custom semgrep, SonarQube string duplication | Repeated string literals across files |
| Config scatter detection | Custom grep/semgrep | Same value hard-coded in multiple locations |

**Hard-coding principle:** Inline values are common in AI output. If a value appears in 3+ files, it should live in one config source. Check: domain knowledge (named constant), environment variance (config/env), existing config home (use consistently).

**Detection patterns:**
```bash
grep -rn '[^a-zA-Z_][0-9]\{2,\}' src/ --include="*.ts" --include="*.py"
grep -rn ':\(3000\|5432\|6379\|8080\|8443\|27017\)' src/
grep -rn 'https\?://[a-z]' src/ --include="*.ts" --include="*.py" | grep -v test | grep -v spec
grep -rn 'timeout.*[0-9]\{4,\}\|retry.*[0-9]' src/
```

## AI008: Implicit Drift

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Version range linting | Custom semgrep/grep, `npm-package-json-lint` | Floating semver ranges beyond patch |
| Docker tag linting | `hadolint`, custom Dockerfile lint | `FROM image:latest` or untagged bases |
| Lockfile enforcement | `npm ci`, `pip install --require-hashes` | Missing or outdated lockfiles |
| Model ID pinning | Custom grep/semgrep | Unpinned model aliases without dated version |
| Infrastructure pin checks | `tflint`, custom Terraform rules | Unpinned provider/module versions |
| GitHub Action pinning | `actionlint`, `pin-github-action` | Actions referenced by tag instead of SHA |
| Renovate/Dependabot presence | Config file check | No automated update mechanism for pinned versions |

**Pinning principle:** A real pin resolves to the same bytes over time. Check both the pin AND an update mechanism (Dependabot, Renovate, scheduled CI).

**Detection patterns:**
```bash
grep -n 'FROM.*:latest\|FROM [^:]*$' Dockerfile*
grep -n '"\^[0-9]\|"~[0-9]\|"\*"\|">=\|">[0-9]' package.json
grep -vn '==\|@' requirements*.txt | grep -v '^#\|^$'
grep -rn 'uses:.*@v[0-9]\|uses:.*@main\|uses:.*@master' .github/
grep -rn 'model.*=.*["'"'"']\(gpt-4\|claude\|sonnet\|opus\|haiku\|gemini\)["'"'"']' src/ | grep -v '\-[0-9]\{4\}'
```

## Minimum Viable Gate Set

For teams starting from zero, recommend in priority order:
1. Type checking (catches AI001)
2. Empty catch lint rules + silent success masking (catches AI004)
3. Mutation testing (catches AI005)
4. Duplication detection (catches AI006)
5. Import boundary enforcement + magic value linting (catches AI007)
6. Dead code detection (catches AI002, AI003)
7. Lockfile enforcement + Docker tag linting (catches AI008)
