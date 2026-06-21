# L2 → L3 Hinge

Most teams stall at L2→L3: ad-hoc agent use does not become safe bounded iteration without
deliberate investment in **shared repo context** paired with **codebase guardrails**.

## Why this transition matters

- Local maxima feel like full adoption — the next step needs explicit investment, not more chat usage.
- **Context is the multiplier**: generic tools need `AGENTS.md`, plans, and CI gates to produce safe output.
- When codegen is fast, the bottleneck shifts to tests, review cycles, and artifacts — address that next.

## Codebase critical path

Load `level-transitions.md` (L2→L3 minimum requirements). Gating categories: typing strength,
testable boundaries, CI reliability.

## Repo enablers (pair with critical-path items)

Load `improvement-actions-agent.md` (Feedforward, Compound engineering, Collaboration sections).
For each codebase requirement, pair one repo enabler:

| Codebase requirement | Repo enabler |
|---------------------|--------------|
| Strict types in CI | Instruction file with 10+ rules + ADR/spec links |
| Reliable, blocking CI | Test-with-code policy in CONTRIBUTING; CI enforces |
| Module boundaries | Boundary linter + agent review checklist in `AGENTS.md` |
| Integration tests on critical paths | `docs/plans/` + first packaged skill for repeatable workflows |
| Merge-blocking checks | PR label/template for agent-assisted work |

Also consider: new-module/API scaffold checklist (handler + test + contract), `docs/runbooks/` for
ops legibility.

## Pairing rule

Pair one Track A item (CI, types, hooks) with one Track B item (workflow artifacts, skills) per
row. See `workflow-and-surfaces.md`.

## Roadmap output

Include the **L2 → L3 hinge** section when **current level ≤ L2 and target level ≥ L3** (the
roadmap must cross the L2→L3 boundary). Add it before High-impact improvements:

```markdown
## L2 → L3 hinge

**Codebase critical path:** [from level-transitions.md]
**Repo enablers:** [paired items from table above]
```
