# Autonomy Levels

## Level definitions

| Level | Name | Description | What agents can safely do |
|-------|------|-------------|---------------------------|
| L0 | Human only | No AI involvement. Fully manual workflows. | Nothing autonomous |
| L1 | Assisted | AI suggests or drafts fragments. Human owns all decisions. | Draft snippets, explain code |
| L2 | Reviewed | Agents make limited changes. Human review before merge. CI may be incomplete. | Small scoped PRs under full human review |
| L3 | Bounded iteration | Agents iterate inside guardrails (scoped tasks, green tests, typed boundaries). Selective human review. | Routine maintenance: bug fixes, tests, docs, dependency upgrades |
| L4 | Verified autonomy | Automated checks are the primary gate. Humans focus on intent and exceptions. | Features inside typed, tested modules; humans review intent |
| L5 | End-to-end autonomous | Machine-readable requirements and strong oracles. Agents plan, implement, and validate with high confidence. | Plan, implement, and validate on specified surfaces |

L3 is the target most teams should aim for first: it is the minimum bar for agents doing
production work unattended on routine tasks.

## Level determination

The level is set by **gates**, not by the score. Load
`../../generate-roadmap/references/level-transitions.md`; each transition lists minimum
requirements, and each requirement maps to one or more signal verdicts.

1. Starting from L1, a level is **unlocked** when at least **80%** of its transition requirements
   pass and every lower level is unlocked.
2. The recommended level is the highest unlocked level.
3. Apply the caps below (spec-first cap, oracle ceiling). Caps only lower the level.
4. Report per-level pass percentages in the **Level gates** table so the reader sees how far the
   next gate is.

## Score-to-level mapping (sanity check)

| Score range | Expected level | Rationale |
|-------------|----------------|-----------|
| 0-15 | L0 | No infrastructure for agent safety |
| 16-35 | L1 | Minimal scaffolding; agents can suggest but not safely act |
| 36-55 | L2 | Basic tests and CI exist; agents can act with human review |
| 56-75 | L3 | Strong tests, types, and CI; agents can iterate within bounds |
| 76-90 | L4 | Comprehensive verification; agents gated by automated checks |
| 91-100 | L5 | Full machine-readable intent and oracles; end-to-end autonomy feasible |

If the gate-derived level and the score-derived level differ by more than one step, say so in the
report and name the signals that cause the gap. The usual case is a high score carried by
documentation while a gating basic (CI on PRs, a runnable test suite) is missing.

## Key differentiators between levels

- **L1 to L2**: CI exists and runs tests; agents can submit PRs for review
- **L2 to L3**: Tests are reliable (not flaky), types are enforced, scoping is clear
- **L3 to L4**: Property tests or contracts cover critical paths; CI is the authority
- **L4 to L5**: Machine-readable specs cover system behavior; oracles exist for all critical paths

## The autonomy ceiling

A high readiness score does **not** by itself justify a high autonomy level. The level a codebase
can safely operate at is **capped by the strength of its verification oracles** — agents inherit
oracle quality directly. Running agents above the ceiling turns the pipeline into an *accelerated
defect delivery system*: more autonomy simply ships wrong code faster.

> Effective autonomy = min(gate-derived level, oracle strength on the changed surface).

Practical rules:

- A category breakdown strong on structure/docs/context but **weak on testable boundaries,
  machine-readable intent, or oracles** caps the recommended level at L3 regardless of the gates.
- Autonomy is per-surface, not global: a well-tested core may sit at L4 while a weakly-tested
  integration sits at L2. Recommend the level for the surface being changed, not a single repo-wide number.
- When oracle strength is unknown or unverified, recommend the **lower** adjacent level and flag
  oracle assessment as the blocker. Pair this with the verification plugin's oracle analysis.

## Alignment note

Include under **Collaboration effectiveness** when a mismatch is detected (otherwise omit or
write "Aligned"):

- **Practices ahead of codebase** — Collaboration infrastructure is strong (PR template/labels,
  agent review rubric, multiple project-local agent skills in `.claude/skills/` or equivalent),
  git history shows agent co-authored commits, or estimated first-pass acceptance is high, but the
  gates stop at L1–L2: warn that agent usage may outpace merge safety; prioritize verification,
  types, and CI before raising autonomy.
- **Codebase ahead of practices** — Gates reach L3+ but collaboration infrastructure is absent
  and workflow artifacts are missing: warn that raising agent autonomy without shared context
  will increase iteration cycles; prioritize `AGENTS.md`, plans dir, and collaboration tracking.

Do not infer org-wide maturity levels — only repo-observable signals.
