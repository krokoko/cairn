# Eval Framework Design

Load `eval-framework-operations.md` for difficulty calibration, automation, and tooling.

## Definition

An eval is a repeatable suite that measures how well an agentic workflow performs in a
specific codebase. It shifts focus from "does the code work?" to "can agents reliably
produce working code here?"

## Why evals matter for verification strategy

Traditional verification checks code correctness. Evals check *agent* correctness —
whether agents consistently produce quality code across diverse tasks. Without evals,
teams rely on anecdotes rather than data to assess whether their verification
infrastructure actually enables autonomous work.

## Components of an eval task

Each eval task requires:

| Component | Purpose | Example |
|-----------|---------|---------|
| Defined input | Reproducible starting state | Prompt, context files, instruction file |
| Success criteria | Automated pass/fail | Tests pass, types check, lint clean, behavior correct |
| Repeatability | Statistical confidence | Same task runs 3-5 times; success rate measured |
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
