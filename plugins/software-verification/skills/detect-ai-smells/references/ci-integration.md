# CI Integration

What a well-configured pipeline looks like for AI smell detection, and how to assess gate placement and fitness function maturity.

## Pipeline Positioning

AI smell gates should be positioned after basic quality and before deployment:

```
types → lint → AI smell gates → tests → security → deploy
```

Smell-specific gates by pipeline stage:

| Stage | Gates | Smells caught |
|-------|-------|---------------|
| Pre-commit | Empty catch lint, commit message lint, magic number lint | AI004, AI007, git hygiene |
| CI - fast | Type check, dead code, import boundaries, version pin check | AI001, AI002, AI003, AI007, AI008 |
| CI - slow | Mutation testing, branch coverage, duplication detection, silent success scan | AI004, AI005, AI006, AI009 |
| PR review | PR template check, test-with-source requirement, Docker tag lint | Git hygiene, AI008 |

## Enforcement Levels

| Level | Meaning | When appropriate |
|-------|---------|-----------------|
| **Blocking** | Fails build, prevents merge | High-severity smells (AI001, AI004) |
| **Warning** | PR annotation, does not block | Medium-severity (AI002, AI003, AI005, AI007, AI008, AI009) |
| **Informational** | Report only, trend tracked | Low-severity (AI006), new gates in trial period |

## Feedback Quality Criteria

A gate produces good feedback for agents when it provides:
- File path and line number
- Which rule was violated (rule ID)
- Why it matters (one-line explanation)
- How to fix (suggestion or link)
- Machine-readable format (SARIF, JUnit XML, JSON)

Assess each gate: does its output include all five? Missing elements reduce agent self-correction ability.

## Fitness Function Patterns

### Per-PR delta (recommended)

Compare smell-related metric on branch vs main. Fail if regression exceeds threshold.

Applicable metrics:
- Mutation score (should not decrease)
- Duplication percentage (should not increase)
- Dead code count (should not increase)
- Import depth maximum (should not increase)
- Unpinned reference count (should not increase)
- Silent success patterns (should not increase)

### Trend tracking (recommended for maturity)

Store metrics over time. Watch for:
- Gradual drift (small per-PR increases that compound)
- Sudden spikes (bulk AI-generated code merged)
- Plateau after gate introduction (gate is working)

### Gate effectiveness measurement

Track per gate:
- How often it fires (too rare = misconfigured, too often = too strict)
- False positive rate (developers overriding/ignoring)
- Time-to-fix after gate fires (indicates feedback quality)

## Maturity Levels

| Level | Description | Indicators |
|-------|-------------|------------|
| 0 | No AI smell gates | No mutation testing, no import limits, basic lint only |
| 1 | Partial coverage | Some gates exist (e.g., empty catch rules) but gaps in 4+ categories |
| 2 | Broad coverage | Gates for 6+ categories, mix of blocking and warning, pinning + fail-fast covered |
| 3 | Fitness function maturity | Trend tracking, per-PR deltas, gate effectiveness measurement, automated update mechanisms for pins |
