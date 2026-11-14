# Generator-Evaluator Patterns

## Definition

The Generator-Evaluator pattern uses two agents in an adversarial loop: one writes
code (generator) and another judges it (evaluator). This can expose mistakes missed by self-review;
the value depends on criteria, information separation, and correlated evaluator/generator errors.

## Why self-verification is insufficient

An agent can write code and tests that agree with each other while both being wrong.
The generator and evaluator must use different perspectives, rubrics, or information
to provide genuine verification pressure.

## Pattern variants

### 1. Generator + Test-Writer (separation of concerns)

The generating agent writes implementation; a separate agent writes tests without
seeing the implementation. Tests can offer a separate interpretation of intent. Shared specification
errors can still make implementation and tests agree on wrong behavior.

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
Check whether the suite detects relevant behavior-changing mutations. Investigate survivors:
they can expose weak assertions, equivalent behavior, or changes outside the claimed scope.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator | Task | Implementation + tests | Normal coding flow |
| Mutant | Implementation | Mutated versions | Subtle, realistic bugs only |
| Verifier | Tests + mutants | Outcomes per mutant | Separate killed, survived, equivalent, timeout, and untested cases |

### 4. N-of-M Consensus (corroboration)

Multiple agents produce solutions without sharing drafts. Compare them against external acceptance
criteria. Agreement can reflect correlated model errors or a shared wrong specification; generation
separation alone does not establish statistical independence or a correctness guarantee.

| Role | Input | Output | Key constraint |
|------|-------|--------|----------------|
| Generator 1..N | Same spec | N implementations | Each works independently, no communication |
| Comparator | N implementations | Consensus areas + divergence | Flags disagreements for review |

## When to apply each variant

| Variant | Best for | Cost considerations | Evidence limit |
|---------|----------|---------------------|----------------|
| Generator + Test-Writer | Features with reviewed specs | Another generation plus reconciliation | Tests may share specification mistakes |
| Generator + Critic | Complex or security-sensitive changes | Review and repair iterations | Findings depend on rubric and reviewer context |
| Generator + Mutant | Critical test decisions | Campaign size and test runtime | Sensitivity to selected mutations only |
| N-of-M Consensus | Exploring alternative implementations | Multiple generations and comparison | Agreement is corroboration, not proof |

## Implementation guidance

### Making separation effective

The evaluator must genuinely bring independent perspective:
- Different system prompt / instruction set
- Focus on failure modes, not confirmation
- Access to spec but NOT to generator's reasoning
- Calibrated rubrics with concrete criteria and independently labeled accepted/rejected controls
- Versioned requirement, prompt/model, fixtures, and oracle revisions
- Separate development feedback from evaluation cases; record repeated exposure and leakage limits

### Cost management

Generator-evaluator is expensive. Apply selectively:
- High-criticality components only
- Security boundaries and auth logic
- Data migration and schema changes
- Public API surface changes

Reserve for cases where the cost of a missed bug exceeds the cost of dual generation.

### Integration with CI

Generator produces a candidate; evaluator supplies tests or critique for review. Run the relevant
gates and retain scoped results before merging. Resolve consequential or ambiguous disagreements
with the designated reviewer; evaluation scores do not authorize tool actions or bypass permissions.

## Related patterns

Strengthens Verification Loop; uses Test Oracle; enables Bounded Autonomy tier assignment; cost-managed via Model Routing (cheaper generator, expensive evaluator).
