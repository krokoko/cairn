# Level Transitions

Requirements for advancing an assessed surface. Load
`../../assess-readiness/references/autonomy-prerequisites.md` for the shared ceilings and L5
gate contract. A transition requires evidence; a score or completed planning document is insufficient.

## L0 to L1: Human only -> Assisted

**Minimum requirements:**
- README exists with basic project description
- At least one source file has type annotations or docstrings
- Project can be built/run with documented steps

**Gating categories:** Documentation, Structure

## L1 to L2: Assisted -> Reviewed

**Minimum requirements:**
- CI pipeline exists and runs on PRs
- Test suite exists with at least basic coverage
- Linting or formatting enforced in CI
- Agents can submit PRs that get reviewed

**Gating categories:** CI reliability, Testable boundaries

## L2 to L3: Reviewed -> Bounded iteration

**Minimum requirements:**
- Critical tests complete reliably; measured flakiness and retry behavior are within a justified budget
- Type checking is enforced (strict mode)
- Clear module boundaries that scope agent changes
- Integration tests cover critical paths
- Required checks block merge on failure

**Gating categories:** Typing strength, Testable boundaries, CI reliability

**Collaboration:** Begin estimating iteration cycles on agent-assisted PRs; optional workflow
artifact dir for active plans.

**L2→L3 hinge:** This transition requires explicit investment — it does not happen organically.
Load `l2-to-l3-hinge.md` for the paired codebase + repo-enabler checklist.

## L3 to L4: Bounded iteration -> Verified autonomy

**Minimum requirements:**
- Property-based tests or contracts cover critical invariants
- Critical claims have relevant, sensitive checks; coverage gaps and thresholds are reviewed in context
- Deterministic environment and deployment (reproducible environment, infrastructure as code)
- Architecture decisions are documented
- CI is the authority for merge decisions
- Strong feedforward surfaces: relevant maintained instructions, qualified boundary checks, pre-commit hooks
- Compound engineering in practice: corrections feed back into durable surfaces
- Workflow artifacts for in-flight work (plans or specs) linked from agent entry docs
- First-pass acceptance estimated or tracked; iteration cycles decreasing on bounded tasks

**Gating categories:** Machine-readable intent, Testable boundaries, Deterministic environment and deployment, Progressive context disclosure, Feedforward surfaces, Compound engineering readiness

## L4 to L5: Verified autonomy -> End-to-end autonomous

**Minimum requirements:**
- Machine-readable specifications for all critical behavior
- Adequate, reviewed oracles cover critical paths under explicit assumptions
- Evidence pipeline: structured verification evidence feeds merge/deploy decisions
- Progressive delivery with automated rollback
- Humans govern intent, oracle changes and high-consequence exceptions
- All hidden state documented and config validated
- Consistent naming and patterns across entire repository
- Structured errors with actionable messages everywhere
- Regenerative components: key modules rebuildable from specs/tests without knowledge loss
- Comprehensive feedforward: computational and document-based controls prevent most errors proactively
- Mature compound engineering: feedback flywheel operational, first-pass acceptance high
- Excellent context friendliness: files sized for agent windows, layered docs, retrieval-optimized naming

**Hard prerequisites:** apply all five canonical IDs from
`../../assess-readiness/references/autonomy-prerequisites.md`, with their evidence and status
rules. All must be `met` for the surface to reach L5. Missing, unknown or inapplicable gates
cap at L4 or below; weak/unknown critical-path oracles can lower the ceiling further.
Do not add category-score thresholds as substitutes for these gates.
