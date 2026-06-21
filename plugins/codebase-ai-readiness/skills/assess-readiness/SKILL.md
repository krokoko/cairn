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

Produce an autonomy maturity map for the target codebase. The output is a `readiness-report.md` file containing a numeric score, category breakdown, workflow artifact summary, collaboration effectiveness assessment (including an alignment note when practices and score diverge), recommended autonomy level, blockers, and a prioritized roadmap.

## Workflow

### Step 1: Discover the codebase

Use Glob and Grep to understand the project:

- Identify language(s) and framework(s) from package manifests (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `pom.xml`, `*.csproj`)
- Find CI configuration (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`)
- Find pre-commit hooks (`.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`, `.git/hooks/`)
- Find test directories (`test/`, `tests/`, `__tests__/`, `*_test.go`, `*_spec.rb`)
- Find documentation (`README.md`, `docs/`, `CHANGELOG.md`, `ADR/`, `adr/`)
- Find type configuration (`tsconfig.json`, `mypy.ini`, `pyrightconfig.json`, `.strict`)
- Find containerization (`Dockerfile`, `docker-compose.yml`, `.devcontainer/`, `flake.nix`, `mise.toml`)
- Find Infrastructure as Code (`cdk.json`, `cdktf.json`, `terraform/`, `*.tf`, `Pulumi.yaml`, `template.yaml` (SAM), `*.bicep`, `cloudformation/`)
- Find schemas and contracts (`*.proto`, `openapi.*`, `*.schema.json`, `swagger.*`)
- Find agent context files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/`)
- Find execution plans (`docs/plans/`, `docs/exec-plans/`, `PLANS.md`)
- Find workflow artifacts: requirements/specs (`docs/requirements/`, `docs/specs/`, `requirements/`), design (`docs/design/`, `design/`), review learnings (`docs/reviews/`, `docs/learnings/`) — load `references/workflow-artifacts.md`
- Find config documentation (`.env.example`, `config.schema.json`)
- Find ownership files (`CODEOWNERS`, `OWNERS`)
- Find module boundary enforcement (`eslint-plugin-boundaries` in config, `deptry`, `madge`, ArchUnit, structural tests)
- Find templates and generators (`plop`, `hygen`, cookiecutter, `.template` files)
- Find agent skills and workflows (`.claude/skills/`, agent skill directories)
- Find agent hooks (agent hook configs, `hooks.json`, post-tool-use automation)
- Measure file size distribution: count lines across source files deterministically (glob source files + `wc -l`, excluding vendored/generated/build dirs), not by eyeballing a few. Report the share of files under 300 lines (the "good" target in category 2.15) and flag outliers over 500 lines. The two thresholds are distinct: 300 is the per-file comprehension target; 500 marks a file large enough to warrant splitting.

### Step 2: Assess each category

Evaluate 15 categories. Load `references/category-definitions.md` and `references/category-definitions-agent.md` for detailed signals. Also load `references/agent-contributor-model.md` for the framing principles.

**2.1 Structure and modularity**
- Directory organization clarity
- Module/package boundaries (separate packages, clear exports)
- Naming conventions consistency
- Absence of circular dependencies
- Architectural isolation (sandboxed execution, containerized components, WASM modules)
- Separation of stable vs experimental services/components
- Mechanically-enforced boundaries (custom linters, structural tests, dependency direction checks in CI)

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
- Shift-left checks present (pre-commit hooks, focused test scripts, watch mode configs)
- Test impact analysis (run only affected tests: pytest-testmon, Jest `--onlyChanged`, Launchable) — keeps feedback fast as agent-generated test volume grows

**2.5 Typing strength**
- Type annotations coverage
- Strict mode enabled (e.g., `strict: true` in tsconfig, `--strict` in mypy)
- Absence of escape hatches (`any`, `type: ignore`, `as unknown`)
- Typed API boundaries (request/response types)

**2.6 Deterministic environment and deployment**
- Reproducible environment (Docker, Nix, devcontainer, mise)
- Seed data or fixtures for local development
- Environment template (`.env.example`, `.env.template`)
- Single-command setup documented
- Infrastructure as Code (AWS CDK, Terraform, Pulumi, CloudFormation, Bicep)
- Deployment codified in version control (not manually provisioned)

**2.7 Architecture decisions**
- ADR directory exists with entries
- Design documents or RFCs
- Clear ownership boundaries (CODEOWNERS)
- Enforced decisions: a documented decision traces to the mechanical check enforcing it (ADR ↔ fitness function/lint rule)
- Living decisions: ADRs carry Status + dates; superseded decisions linked, not deleted

**2.8 Machine-readable intent**

Load `references/spec-first-artifacts.md` for the spec-first checklist, scoring bands, and cap rule.

- Schemas (JSON Schema, protobuf, OpenAPI, GraphQL SDL)
- Contracts (pre/postconditions, invariants, assertions)
- Property-based tests
- Formal specifications (TLA+, Alloy)
- Configuration schemas with validation
- Executable acceptance criteria (EARS-style requirements turned into Gherkin/BDD scenarios)
- **Spec-first artifacts**: stable requirement IDs (`REQ-*.md`, `spec/requirements/`), Gherkin scenario per active requirement, pure core separated from IO/adapters, determinism ports where simulation applies
- Requirement traceability — guards against intent drift. File-based signals (requirement dirs, tests tagging requirement IDs, a requirement-coverage report) are found with Glob/Grep; the PR→issue link signal lives in git history, so check it with `git log` (closing keywords like `Closes #123`, bare `#123`, or tracker keys). If git history is unavailable, mark the PR-link signal "not inspectable" rather than scoring it absent.
- Regenerative readiness (components definable by specs/tests, rebuildable without loss)

Apply the **cap rule** from spec-first-artifacts when scoring: strong schemas/property tests without requirement files or executable criteria → cap 2.8 at 60.

**2.9 Progressive context disclosure**
- AGENTS.md or equivalent agent-specific context file
- Layered documentation (root README -> CONTRIBUTING -> per-folder READMEs)
- Cross-links between documents
- Clear entry point for newcomers (human or agent)
- Plans as first-class versioned artifacts (execution plans, progress logs, decision logs in-repo)
- Agent context file links to the decision corpus (ADRs, specs, `.feature` files), not just file locations

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
- Lint/CI error messages contain agent-targeted remediation instructions (what to fix, not just what failed)

**2.13 Feedforward surfaces**

Load `references/feedforward-surfaces.md` for detailed scoring signals.

- Instruction files with project-specific rules (CLAUDE.md, AGENTS.md) — count actionable rules
- Strict type checking with few escape hatches
- Module boundary enforcement via linter or structural tests
- Pre-commit hooks running type checker + linter + formatter per-file
- Non-bypassable hooks (agent config denies `--no-verify`; branch protection enforces checks server-side)
- Templates and generators for common file patterns
- Security scanners in pre-commit or per-file hooks

**2.14 Compound engineering readiness**

Load `references/compound-engineering.md` and `references/workflow-artifacts.md` for detailed scoring signals.

- Instruction file with evidence of iterative growth (>10 rules, recently updated)
- Custom skills or packaged workflows for repeated tasks
- Workflow artifact directories (plans, specs, design, review notes) with recent, feature-scoped content
- Hooks that enforce conventions discovered through past mistakes
- Tests encoding past bugs as regression checks
- Evidence of maintenance (recent updates, hooks matching current tooling)
- Durable surfaces exist where lessons can land (not just ephemeral chat/PR comments)

**2.15 Context engineering friendliness**

Load `references/context-engineering.md` for detailed scoring signals.

- File size distribution: 90%+ files under 300 lines (good), many >500 lines (problematic)
- Layered documentation from root README to module-level docs
- Clear entry points and explicit module exports
- Retrieval-friendly naming: no generic names (utils, helpers, misc), consistent terms
- Structured headings in documentation for searchability

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

If category **2.8 Machine-readable intent** is below 51 or spec-first artifacts are absent (no
requirement files, no executable acceptance criteria per `references/spec-first-artifacts.md`), apply
the autonomy **cap rule**: recommended level must not exceed **L3** regardless of weighted score.
Note spec-first gaps in blockers.

### Step 6: Identify blockers

For the current autonomy level, identify what specifically prevents moving to the next level. Be concrete: name missing files, missing configurations, weak categories.

### Step 7: Assess collaboration effectiveness

Load `references/collaboration-metrics.md`. Estimate or mark "not measured" for first-pass
acceptance, iteration cycles per task, and post-merge rework. Note infrastructure enablers
(PR templates, labels, review rubrics, learning docs). Produce 2-4 recommendations to start
or improve tracking aligned with the recommended autonomy level. Apply the **Alignment note**
from `references/autonomy-levels.md` when collaboration signals and score diverge.

### Step 8: Generate roadmap

Produce a prioritized list of 5-10 recommended actions. For each action:
- What to do (specific and actionable)
- Which category it improves
- Estimated effort (small/medium/large)
- Expected score impact

When the recommended autonomy level is **L2**, load
`../generate-roadmap/references/l2-to-l3-hinge.md` and prioritize paired codebase +
repo-enabler items in the roadmap table.

If Step 7 flagged **practices ahead of codebase**, weight actions toward verification, types,
and CI. If **codebase ahead of practices**, weight toward `AGENTS.md`, plans dir, and
collaboration tracking from the hinge repo-enabler table.

### Step 9: Write the report

Write `readiness-report.md` in the codebase root. Load `references/report-template.md` for the
required sections and tables. Write the **Alignment note** under **Collaboration effectiveness**
after completing Step 7.
