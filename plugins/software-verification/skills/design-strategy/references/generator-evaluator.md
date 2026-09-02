# Generator-Evaluator Patterns

## When to use this vs verifier-guided search

| Situation | Pattern |
|-----------|---------|
| Deterministic verifier available | **Verifier-guided search** — load `verifier-guided-search.md` |
| No deterministic verifier; need adversarial pressure | **Generator-evaluator** (this document) |
| Ranking multiple passing candidates | **Candidate selection policy** — load `candidate-selection-policy.md` |

**Core rule (verifier-guided search):** An LLM evaluator may critique. It must not be the final
correctness authority when a deterministic verifier is available.

## Definition

The Generator-Evaluator pattern uses two agents in an adversarial loop: one writes code (generator)
and another judges it (evaluator). This creates verification pressure beyond self-review, since
agents tend to be biased toward their own output.

## Why self-verification is insufficient

An agent can write code and tests that agree with each other while both being wrong. The generator
and evaluator must use different perspectives, rubrics, or information to provide genuine
verification pressure.

## Pattern variants

### 1. Generator + Test-Writer (separation of concerns)

The generating agent writes implementation; a separate agent writes tests without seeing the
implementation. Tests express intent independently, catching cases where
implementation and tests silently agree on wrong behavior.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator | Spec/requirements | Implementation code | Cannot see evaluator's tests |
| Evaluator | Spec/requirements | Test suite | Cannot see generator's implementation |
| Arbiter | Both outputs | Pass/fail + diagnostics | Runs tests against implementation |

### 2. Generator + Critic (adversarial review)

One agent generates code; another reviews against a rubric. The generator fixes identified issues.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator | Task + context | Code change | Normal coding agent |
| Critic | Code change + rubric | Issue list | Must seek problems, not confirm quality |
| Generator (round 2) | Issue list | Fixes | Addresses critic's findings |

### 3. Generator + Mutant (robustness testing)

After the generator produces code, a mutant agent deliberately introduces subtle bugs.
The test suite must catch them. If mutations survive, tests are weak.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator | Task | Implementation + tests | Normal coding flow |
| Mutant | Implementation | Mutated versions | Subtle, realistic bugs only |
| Verifier | Tests + mutants | Kill rate | Measures test strength |

### 4. N-of-M Consensus (statistical verification)

Multiple generators produce independent solutions; agreement provides confidence. When a
deterministic verifier exists, **filter to verifier-passing candidates first**, then compare.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator 1..N | Same spec | N implementations | Independent, no communication |
| Verifier | N implementations | Eligible subset | Mandatory properties — see `candidate-selection-policy.md` |
| Comparator | Eligible subset | Consensus + divergence | Flags disagreements for review |

## When to apply each variant

| Variant | Best for | Cost | Confidence gain |
|---------|----------|------|-----------------|
| Generator + Test-Writer | New features with clear specs | 2x | High (independent verification) |
| Generator + Critic | Complex changes, security-sensitive | 1.5x | Medium (reviewer bias possible) |
| Generator + Mutant | Testing test quality itself | 2-3x | High for test adequacy |
| N-of-M Consensus | Critical, well-specified components | Nx | Highest when verifier filters first |

## Mandatory vs objectives in search

When multiple candidates pass the verifier, rank them with the lexicographic rule in
`candidate-selection-policy.md` (the canonical statement). Do not restate the policy here.

## Implementation guidance

### Making separation effective

The evaluator must genuinely bring independent perspective:
- Different system prompt / instruction set
- Focus on failure modes, not confirmation
- Access to spec but NOT to generator's reasoning
- Calibrated rubrics with concrete criteria (not "looks good")

### Protecting evaluators from tampering

Load `oracle-integrity.md`. Evaluators (tests, specs, verifier configs) must be:
- Outside agent write scope or protected by review gate
- Checked for coordinated impl + oracle changes (AI012)

### Cost management

Apply selectively:
- High-criticality components
- Security boundaries and auth logic
- Data migration and schema changes
- Public API surface changes

Reserve for cases where the cost of a missed bug exceeds the cost of dual generation.

### Integration with CI

1. Generator produces code; evaluator produces tests or critique
2. **Deterministic verifier** (CI) is authoritative arbiter
3. LLM evaluator output is advisory only when verifier exists
4. Disagreements between LLM evaluator and verifier → verifier wins; human on ambiguity
5. Candidate selection uses mandatory-then-objectives ranking

## Related patterns

- `verifier-guided-search.md` — primary pattern for L4/L5 autonomous search
- `candidate-selection-policy.md` — mandatory vs optimization objectives
- `oracle-integrity.md` — anti-evaluator-gaming
- Strengthens Verification Loop; enables Bounded Autonomy; cost-managed via Model Routing
