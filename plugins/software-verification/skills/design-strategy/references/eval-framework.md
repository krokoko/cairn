# Eval Framework Design

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

### Phase 2: Difficulty spectrum

Calibrate tasks across the difficulty range:

| Difficulty | Human time | Example |
|------------|-----------|---------|
| Trivial | <5 min | Fix typo, update version, add import |
| Easy | 5-30 min | Add test, fix lint error, small refactor |
| Medium | 30 min - 2 hr | Implement feature, fix bug, add integration |
| Hard | 2-8 hr | Cross-module refactor, new system, complex bug |
| Beyond horizon | >8 hr | Architecture change, major migration |

### Phase 3: Automation

Run evals:
- After model/harness updates
- After instruction file changes
- After tool or skill additions
- Weekly for regression detection

## Eval output format

```markdown
# Eval Results — [Date]

## Summary
- Tasks attempted: N
- Success rate: X%
- Average iterations: Y
- Average tokens: Z

## Per-task results

| Task | Difficulty | Result | Iterations | Notes |
|------|-----------|--------|------------|-------|
| ... | ... | Pass/Fail | N | ... |

## Regressions
[Tasks that previously passed but now fail]

## Improvements
[Tasks that previously failed but now pass]
```

## Relationship to verification infrastructure

Evals consume verification infrastructure:
- Tests provide correctness oracles
- Type checkers provide structural oracles
- Linters provide convention oracles
- CI provides integration oracles

Low eval scores indicate either:
1. Weak verification infrastructure (no oracle to check against)
2. Poor feedforward surfaces (agent makes preventable mistakes)
3. Task horizon exceeded (task too complex for single agent session)

## Tools for building evals

| Tool | Language | Notes |
|------|----------|-------|
| Custom scripts | Any | Run agent, check git diff, run tests |
| SWE-bench format | Python | Standard format for coding task evals |
| Braintrust | Any | Eval platform with scoring and comparison |
| OpenAI Evals | Any | Framework for structured eval suites |
| Terminal Bench | CLI | Terminal-based agent benchmark |
