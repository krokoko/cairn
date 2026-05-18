# Generator-Evaluator Patterns

## Definition

The Generator-Evaluator pattern uses two agents in an adversarial loop: one writes
code (generator) and another judges it (evaluator). This creates verification
pressure beyond what self-review provides, since agents tend to be biased toward
their own output.

## Why self-verification is insufficient

An agent can write code and tests that agree with each other while both being wrong.
The generator and evaluator must use different perspectives, rubrics, or information
to provide genuine verification pressure.

## Pattern variants

### 1. Generator + Test-Writer (separation of concerns)

The generating agent writes implementation; a separate agent writes tests without
seeing the implementation. Tests express intent independently, catching cases where
implementation and tests silently agree on wrong behavior.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator | Spec/requirements | Implementation code | Cannot see evaluator's tests |
| Evaluator | Spec/requirements | Test suite | Cannot see generator's implementation |
| Arbiter | Both outputs | Pass/fail + diagnostics | Runs tests against implementation |

### 2. Generator + Critic (adversarial review)

One agent generates code; another reviews it against a rubric, attempting to find
issues. The generator then fixes identified issues.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator | Task + context | Code change | Normal coding agent |
| Critic | Code change + rubric | Issue list | Must actively seek problems, not confirm quality |
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

Multiple generator agents produce independent solutions. Solutions are compared;
agreement across independent generations provides confidence.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator 1..N | Same spec | N implementations | Each works independently, no communication |
| Comparator | N implementations | Consensus areas + divergence | Flags disagreements for review |

## When to apply each variant

| Variant | Best for | Cost | Confidence gain |
|---------|----------|------|-----------------|
| Generator + Test-Writer | New features with clear specs | 2x generation cost | High (independent verification) |
| Generator + Critic | Complex changes, security-sensitive | 1.5x cost | Medium (reviewer bias possible) |
| Generator + Mutant | Testing test quality itself | 2-3x cost | High for test adequacy |
| N-of-M Consensus | Critical, well-specified components | Nx cost | Highest (statistical) |

## Implementation guidance

### Making separation effective

The evaluator must genuinely bring independent perspective:
- Different system prompt / instruction set
- Focus on failure modes, not confirmation
- Access to spec but NOT to generator's reasoning
- Calibrated rubrics with concrete criteria (not "looks good")

### Cost management

Generator-evaluator is expensive. Apply selectively:
- High-criticality components only
- Security boundaries and auth logic
- Data migration and schema changes
- Public API surface changes

Reserve for cases where the cost of a missed bug exceeds the cost of dual generation.

### Integration with CI

Generator-evaluator can feed into standard CI:
1. Generator produces code
2. Evaluator produces independent tests or critique
3. Both merge into PR
4. Standard CI validates the combination
5. Disagreements flagged for human review

## Relationship to other verification patterns

- **Strengthens**: Verification Loop (adds independent check within the loop)
- **Uses**: Test Oracle (evaluator needs oracle to judge against)
- **Enables**: Higher confidence in Bounded Autonomy tier assignment
- **Cost-managed by**: Model Routing (use cheaper model for generator, expensive for evaluator)
