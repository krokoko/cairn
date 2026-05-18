---
name: assess-readiness
description: |
  Assess the AI readiness of a codebase and produce an autonomy maturity map.
  Trigger phrases: "assess readiness", "how AI-friendly is this codebase",
  "autonomy maturity", "readiness score", "AI readiness assessment",
  "how ready is my codebase for AI agents"
argument-hint: "[path-to-codebase] (defaults to current directory)"
allowed-tools: Read Bash Glob Grep
user-invocable: true
---

# Codebase AI Readiness Assessment

Produce an autonomy maturity map for the target codebase. The output is a `readiness-report.md` file containing a numeric score, category breakdown, recommended autonomy level, blockers, and a prioritized roadmap.

## Workflow

### Step 1: Discover the codebase

Use Glob and Grep to understand the project:

- Identify language(s) and framework(s) from package manifests (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `pom.xml`, `*.csproj`)
- Find CI configuration (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`)
- Find test directories (`test/`, `tests/`, `__tests__/`, `*_test.go`, `*_spec.rb`)
- Find documentation (`README.md`, `docs/`, `CHANGELOG.md`, `ADR/`, `adr/`)
- Find type configuration (`tsconfig.json`, `mypy.ini`, `pyrightconfig.json`, `.strict`)
- Find containerization (`Dockerfile`, `docker-compose.yml`, `.devcontainer/`, `flake.nix`, `mise.toml`)
- Find schemas and contracts (`*.proto`, `openapi.*`, `*.schema.json`, `swagger.*`)
- Find agent context files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/`)
- Find config documentation (`.env.example`, `config.schema.json`)
- Find ownership files (`CODEOWNERS`, `OWNERS`)

### Step 2: Assess each category

Evaluate 12 categories. Load `references/category-definitions.md` for detailed signals. Also load `references/agent-contributor-model.md` for the framing principles.

**2.1 Structure and modularity**
- Directory organization clarity
- Module/package boundaries (separate packages, clear exports)
- Naming conventions consistency
- Absence of circular dependencies

**2.2 Documentation**
- README presence and completeness
- Inline documentation / docstrings
- API documentation (generated or manual)
- Architecture Decision Records
- CHANGELOG or commit convention

**2.3 Testable boundaries**
- Test file count vs source file count (ratio)
- Test isolation (unit vs integration separation)
- Dependency injection or seam patterns
- Mock/stub usage and quality

**2.4 CI reliability**
- CI config exists and is non-trivial
- Number of distinct checks/jobs
- Coverage reporting configured
- Required/protected branch checks
- Evidence of flakiness (retry configs, `flaky` labels)

**2.5 Typing strength**
- Type annotations coverage
- Strict mode enabled (e.g., `strict: true` in tsconfig, `--strict` in mypy)
- Absence of escape hatches (`any`, `type: ignore`, `as unknown`)
- Typed API boundaries (request/response types)

**2.6 Deterministic local setup**
- Reproducible environment (Docker, Nix, devcontainer, mise)
- Seed data or fixtures for local development
- Environment template (`.env.example`, `.env.template`)
- Single-command setup documented

**2.7 Architecture decisions**
- ADR directory exists with entries
- Design documents or RFCs
- Clear ownership boundaries (CODEOWNERS)

**2.8 Machine-readable intent**
- Schemas (JSON Schema, protobuf, OpenAPI, GraphQL SDL)
- Contracts (pre/postconditions, invariants, assertions)
- Property-based tests
- Formal specifications (TLA+, Alloy)
- Configuration schemas with validation

**2.9 Progressive context disclosure**
- AGENTS.md or equivalent agent-specific context file
- Layered documentation (root README -> CONTRIBUTING -> per-folder READMEs)
- Cross-links between documents
- Clear entry point for newcomers (human or agent)

**2.10 Hidden state and magic**
- Environment variables documented in one place (`.env.example`, config schema)
- No implicit defaults that change behavior across environments
- Feature flags and runtime config are explicit and documented
- No framework "magic" without corresponding documentation

**2.11 Repository-scale reasoning**
- Consistent naming across modules (same concept = same term)
- No synonyms for the same abstraction (handler/processor/manager)
- Predictable file patterns (same structure in each module)
- Retrieval-friendly organization (clear headings, structured docs)

**2.12 Failure mode legibility**
- No swallowed exceptions or silent fallbacks
- Error messages include what failed, where, and what to do next
- Failures are loud and early (fail-fast patterns)
- Logging is structured and actionable

### Step 3: Score each category

Load `references/scoring-rubric.md` for scoring criteria.

Assign each category a score from 0-100:
- 0-25: Absent or minimal
- 26-50: Basic, inconsistent
- 51-75: Good, mostly consistent
- 76-100: Excellent, systematic

### Step 4: Calculate overall score

Use the category weights from the scoring rubric to compute a weighted average (0-100).

### Step 5: Determine autonomy level

Load `references/autonomy-levels.md` and map the overall score to L0-L5.

### Step 6: Identify blockers

For the current autonomy level, identify what specifically prevents moving to the next level. Be concrete: name missing files, missing configurations, weak categories.

### Step 7: Generate roadmap

Produce a prioritized list of 5-10 recommended actions. For each action:
- What to do (specific and actionable)
- Which category it improves
- Estimated effort (small/medium/large)
- Expected score impact

### Step 8: Write the report

Write the file `readiness-report.md` in the codebase root with this structure:

```markdown
# AI Readiness Report

## Overall Score

**Score: XX/100**

## Recommended Autonomy Level

**Level: LX — [Level Name]**

## Category Breakdown

| Category | Score | Notes |
|----------|-------|-------|
| Structure and modularity | XX | ... |
| Documentation | XX | ... |
| Testable boundaries | XX | ... |
| CI reliability | XX | ... |
| Typing strength | XX | ... |
| Deterministic local setup | XX | ... |
| Architecture decisions | XX | ... |
| Machine-readable intent | XX | ... |
| Progressive context disclosure | XX | ... |
| Hidden state and magic | XX | ... |
| Repository-scale reasoning | XX | ... |
| Failure mode legibility | XX | ... |

## Blockers

[List of specific blockers preventing advancement to next level]

## Roadmap

| Priority | Action | Category | Effort | Impact |
|----------|--------|----------|--------|--------|
| 1 | ... | ... | ... | ... |
```
