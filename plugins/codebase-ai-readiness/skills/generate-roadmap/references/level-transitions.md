# Level Transitions

Requirements for advancing from one autonomy level to the next. These lists are also the **level
gates** used by `assess-readiness`: a level unlocks when at least 80% of its applicable
requirements pass (round up) and every lower level is unlocked (see the assess skill's
`autonomy-levels.md`). Every requirement is observable and maps to signal rows in the assess
skill's category tables. Requirements marked *(services)* are N/A for libraries and CLIs and leave
the denominator. A requirement whose signals are NOT INSPECTABLE counts as not passed.

**Gating categories** name where most of a transition's requirements live. They steer roadmap
weighting; they are not part of the unlock rule.

## L0 to L1: Human only -> Assisted

**Requirements:**
- README exists with a project description
- Build and run steps are documented
- At least one source module carries type annotations or docstrings

**Gating categories:** Documentation, Structure

## L1 to L2: Assisted -> Reviewed

**Requirements:**
- CI pipeline runs on pull requests
- Test suite exists and runs with a documented command
- Linting or formatting enforced in CI
- Dependencies pinned with a committed lockfile
- Changes land through reviewed pull requests (PR template, CODEOWNERS, or protected default branch)

**Gating categories:** CI reliability, Testable boundaries

## L2 to L3: Reviewed -> Bounded iteration

**Requirements:**
- Flakiness contained: no blanket retries; flaky tests quarantined or tracked
- Type checking enforced in strict mode in CI
- Module boundaries enforced mechanically, or documented per module
- Integration tests exist for critical paths
- Required checks block merge (branch protection or rulesets)
- Pre-commit hooks give per-file feedback before CI
- Instruction file exists with project-specific rules
- Dependency update automation configured
- Secret scanning runs in pre-commit or CI
- Structured logging and health checks *(services)*

**Gating categories:** Typing strength, Testable boundaries, CI reliability

**Practice (informative, from Collaboration effectiveness):** begin estimating iteration cycles on
agent-assisted PRs; optional workflow artifact dir for active plans.

**L2→L3 hinge:** This transition requires explicit investment — it does not happen organically.
Load `l2-to-l3-hinge.md` for the paired codebase + repo-enabler checklist.

## L3 to L4: Bounded iteration -> Verified autonomy

**Requirements:**
- Property-based tests or contracts cover critical invariants
- Coverage tracked and enforced above a threshold in CI
- Reproducible environment (container, Nix, devcontainer, or mise)
- Infrastructure as Code in version control *(services)*
- ADRs exist with status and dates
- Instruction file with >10 rules, module boundary enforcement, and non-bypassable hooks
- Instruction file validated by a CI job or hook that runs its commands
- Essential CI feedback measured under 10 minutes
- Error tracking, tracing, and runbooks *(services)*
- Workflow artifacts (plans or specs) exist and are linked from agent entry docs
- Regression tests reference past bugs and hooks encode past corrections
- PR template or labels identify agent-assisted work

**Gating categories:** Machine-readable intent, Testable boundaries, Deterministic environment and deployment, Progressive context disclosure, Feedforward surfaces, Compound engineering readiness

**Practice (informative):** first-pass acceptance estimated or tracked; iteration cycles decreasing
on bounded tasks.

## L4 to L5: Verified autonomy -> End-to-end autonomous

**Requirements:**
- Requirement files with stable IDs and an executable acceptance scenario per active requirement
- Requirement ↔ test ↔ code traceability enforced by a gate
- Oracles on every critical path (exact, property, statistical, or LLM-as-judge)
- Evidence pipeline: structured verification output consumed by merge and deploy decisions
- Progressive delivery with automated rollback *(services)*
- All configuration validated by a schema; every environment variable documented
- Consistent naming and predictable module patterns across the repository
- Structured errors with actionable messages everywhere
- Regenerative components: key modules rebuildable from specs and tests alone
- Every feedforward surface row passes
- 90%+ of source files under 300 lines with layered documentation

**Gating categories:** Machine-readable intent, Feedforward surfaces

**Hard prerequisites (a cap, all required — L5 is gated by the weakest, not the average):**
At L5 humans leave the code-review loop entirely, so the safety net is the oracle, not a reviewer.
Treat these as pass/fail gates on top of the 80% rule:

- [ ] Codified, **executable** specifications for all critical behavior (not prose — runnable: BDD/Gherkin, contracts, schemas)
- [ ] A **strong oracle on every critical path** (machine-checkable and deterministic — see the verification plugin's oracle analysis; weak/brittle oracles do not count)
- [ ] A **reliable simulation/staging environment** that mirrors production closely enough to trust pre-merge validation
- [ ] Telemetry rich enough to detect **silent failures** — wrong-but-not-crashing behavior — not just exceptions and downtime
- [ ] Progressive delivery with **automated rollback** triggered by that telemetry

If any prerequisite is missing, the codebase is not L5-ready regardless of the gate percentage:
agents would ship defects faster than the (now absent) human reviewer could have caught them.
Recommend staying at L4 and closing the missing prerequisite first.
