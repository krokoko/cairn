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
