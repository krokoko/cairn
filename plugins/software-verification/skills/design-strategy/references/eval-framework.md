# Eval Framework Design

Load `eval-framework-operations.md` for difficulty calibration, automation, and tooling.

## Definition

An eval is a repeatable suite that measures how well an agentic workflow performs in a
specific codebase. It shifts focus from "does the code work?" to "can agents reliably
produce working code here?"

## Why evals matter for verification strategy

Code checks support scoped claims. Evals measure an agent workflow on declared tasks and criteria,
with results depending on fixture quality, model/configuration, and sampling. Without evals,
teams rely on anecdotes rather than data to assess whether their verification
infrastructure actually enables autonomous work.

## Components of an eval task

Each eval task requires:

| Component | Purpose | Example |
|-----------|---------|---------|
| Defined input | Reproducible starting state | Prompt, context files, instruction file |
| Success criteria | Automated pass/fail | Tests pass, types check, lint clean, behavior correct |
| Repeatability | Estimate variability | Record repeated attempts, sample size, and uncertainty |
| Difficulty calibration | Horizon mapping | Task annotated with estimated human-expert time |

## Measurement dimensions

| Dimension | What it measures | How to check |
|-----------|-----------------|--------------|
| Correctness | Does output pass all tests? | Run test suite, type checker, linter |
| Convention adherence | Does output follow project standards? | Instruction file rules satisfied; no lint violations |
| Efficiency | How many iterations/tool calls? | Count agent turns, tool calls, tokens consumed |
| Robustness | Does agent handle edge cases? | Tasks with ambiguous requirements, missing context |
| Self-correction | Does agent fix its own mistakes? | Count failures followed by successful fixes |
| Scope discipline | Does agent stay within task bounds? | Check for unnecessary changes outside task scope |

## Building strategy

### Phase 1: Seed tasks (5-10 representative tasks)

Draw from actual project history:
- A recent bug fix (regression + fix)
- A recent feature addition (new file + tests)
- A refactoring task (behavior-preserving change)
- A configuration change (CI, dependency, tooling)
- A documentation update (README, API docs)

For each, record:
- The prompt that would trigger the work
- The files that should change
- The tests that validate correctness
- The estimated human-expert time

## Independent evaluation and maintenance tasks

Include independently authored accepted/rejected controls and prohibited conclusions, not only
tests copied from the implementation. For an assessment skill, examples include configured-but-not-run
checks, stale reports, skipped linked tests, equivalent surviving mutations, and local-only evidence.
Keep format validation separate from semantic adjudication of the findings.

For maintainability, ask for a representative change through an intended extension point. Record
unexpected edits, effort, regressions, and boundary violations. Improved metrics alone do not show that
the change became easier. Define acceptable behavioral differences explicitly for refactors.

Version source fixtures, requirements, oracle labels, model, prompts, and tool configuration. Separate
development cases from evaluation cases where practical; repeated feedback can weaken held-out status.
Evaluate model judges against independent labels including allowed and rejected outcomes. A sample's
success does not establish general reliability or authorize actions.
