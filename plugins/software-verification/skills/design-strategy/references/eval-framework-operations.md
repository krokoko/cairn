# Eval Framework (Operations)

Continues `eval-framework.md`. Difficulty calibration, automation, output format, and tooling.

## Phase 2: Difficulty spectrum

Calibrate tasks across the difficulty range:

| Difficulty | Human time | Example |
|------------|-----------|---------|
| Trivial | <5 min | Fix typo, update version, add import |
| Easy | 5-30 min | Add test, fix lint error, small refactor |
| Medium | 30 min - 2 hr | Implement feature, fix bug, add integration |
| Hard | 2-8 hr | Cross-module refactor, new system, complex bug |
| Beyond horizon | >8 hr | Architecture change, major migration |

## Phase 3: Automation

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

Evals consume verification infrastructure (tests, types, lint, CI). Low eval scores indicate:
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
