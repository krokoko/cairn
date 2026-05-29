# Level Transitions

Requirements for advancing from one autonomy level to the next.

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
- Tests are reliable (flake rate < 5%)
- Type checking is enforced (strict mode)
- Clear module boundaries that scope agent changes
- Integration tests cover critical paths
- Required checks block merge on failure

**Gating categories:** Typing strength, Testable boundaries, CI reliability

**Collaboration:** Begin estimating iteration cycles on agent-assisted PRs; optional workflow
artifact dir for active plans.

## L3 to L4: Bounded iteration -> Verified autonomy

**Minimum requirements:**
- Property-based tests or contracts cover critical invariants
- Coverage is tracked and enforced above a threshold
- Deterministic environment and deployment (reproducible environment, infrastructure as code)
- Architecture decisions are documented
- CI is the authority for merge decisions
- Strong feedforward surfaces: instruction file with >10 rules, module boundary enforcement, pre-commit hooks
- Compound engineering in practice: corrections feed back into durable surfaces
- Workflow artifacts for in-flight work (plans or specs) linked from agent entry docs
- First-pass acceptance estimated or tracked; iteration cycles decreasing on bounded tasks

**Gating categories:** Machine-readable intent, Testable boundaries, Deterministic environment and deployment, Progressive context disclosure, Feedforward surfaces, Compound engineering readiness

## L4 to L5: Verified autonomy -> End-to-end autonomous

**Minimum requirements:**
- Machine-readable specifications for all critical behavior
- Oracles exist for all critical paths (exact, property, statistical, or LLM-as-judge)
- Evidence pipeline: structured verification evidence feeds merge/deploy decisions
- Progressive delivery with automated rollback
- Human review limited to exceptions and architecture changes
- All hidden state documented and config validated
- Consistent naming and patterns across entire repository
- Structured errors with actionable messages everywhere
- Regenerative components: key modules rebuildable from specs/tests without knowledge loss
- Comprehensive feedforward: computational and document-based controls prevent most errors proactively
- Mature compound engineering: feedback flywheel operational, first-pass acceptance high
- Excellent context friendliness: files sized for agent windows, layered docs, retrieval-optimized naming

**Gating categories:** Machine-readable intent (must be 90+), Feedforward surfaces (must be 85+), all other categories 75+
