# Autonomy Levels

## Level definitions

| Level | Name | Description |
|-------|------|-------------|
| L0 | Human only | No AI involvement. Fully manual workflows. |
| L1 | Assisted | AI suggests or drafts fragments. Human owns all decisions. |
| L2 | Reviewed | Agents make limited changes. Human review before merge. CI may be incomplete. |
| L3 | Bounded iteration | Agents iterate inside guardrails (scoped tasks, green tests, typed boundaries). Selective human review. |
| L4 | Verified autonomy | Automated checks are the primary gate. Humans focus on intent and exceptions. |
| L5 | End-to-end autonomous | Machine-readable requirements and strong oracles. Agents plan, implement, and validate with high confidence. |

## Score-to-level mapping

| Score range | Recommended level | Rationale |
|-------------|-------------------|-----------|
| 0-15 | L0 | No infrastructure for agent safety |
| 16-35 | L1 | Minimal scaffolding; agents can suggest but not safely act |
| 36-55 | L2 | Basic tests and CI exist; agents can act with human review |
| 56-75 | L3 | Strong tests, types, and CI; agents can iterate within bounds |
| 76-90 | L4 | Comprehensive verification; agents gated by automated checks |
| 91-100 | L5 | Full machine-readable intent and oracles; end-to-end autonomy feasible |

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

> Effective autonomy = min(readiness score → level, oracle strength on the changed surface).

Practical rules:

- A category breakdown strong on structure/docs/context but **weak on testable boundaries,
  machine-readable intent, or oracles** caps the recommended level at L3 regardless of the weighted score.
- Autonomy is per-surface, not global: a well-tested core may sit at L4 while a weakly-tested
  integration sits at L2. Recommend the level for the surface being changed, not a single repo-wide number.
- When oracle strength is unknown or unverified, recommend the **lower** adjacent level and flag
  oracle assessment as the blocker. Pair this with the verification plugin's oracle analysis.
