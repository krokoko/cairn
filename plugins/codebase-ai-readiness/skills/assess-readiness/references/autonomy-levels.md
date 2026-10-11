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

## Provisional score-to-level mapping

The score is an editorial diagnostic, not a probability of correctness or authorization.
Apply `autonomy-prerequisites.md` to every surface before recommending an operating level.

| Score range | Provisional level | Profile to investigate |
|-------------|-------------------|-----------|
| 0-15 | L0 | No infrastructure for agent safety |
| 16-35 | L1 | Minimal scaffolding; agents can suggest but not safely act |
| 36-55 | L2 | Basic tests and CI exist; agents can act with human review |
| 56-75 | L3 | Strong tests, types, and CI; agents can iterate within bounds |
| 76-90 | L4 | Broad controls are visible; verify their adequacy and execution |
| 91-100 | L5 | Strong signals; all hard prerequisites still require scoped evidence |

## Key differentiators between levels

- **L1 to L2**: CI exists and runs tests; agents can submit PRs for review
- **L2 to L3**: Tests are reliable (not flaky), types are enforced, scoping is clear
- **L3 to L4**: Property tests or contracts cover critical paths; CI is the authority
- **L4 to L5**: Machine-readable specs cover system behavior; oracles exist for all critical paths

## The autonomy ceiling

A high readiness score does **not** by itself justify a high autonomy level. Evaluate the
adequacy of the oracle for the specific claim, the current run evidence, dependency fidelity
and recovery controls. A method name or universal "oracle strength" ranking cannot replace
that assessment.

> Recommended autonomy = min(provisional score level, evidence ceiling on the changed surface).

Practical rules:

- Apply the caps and five L5 gates from `autonomy-prerequisites.md`; strong documentation
  cannot compensate for weak or unknown evidence on a critical path.
- Autonomy is per-surface, not global: a well-tested core may sit at L4 while a weakly-tested
  integration sits at L2. Recommend the level for the surface being changed, not a single repo-wide number.
- When a critical oracle is unknown or unverified, recommend at most L3 and flag its
  assessment as a blocker. Lower the ceiling further if reliable bounded iteration is unproven.
- Keep operational permissions separate: the report does not approve merge, deploy or tool access.

## Alignment note

Include under **Collaboration effectiveness** when a mismatch is detected (otherwise omit or
write "Aligned"):

- **Practices ahead of codebase** — Collaboration infrastructure is strong (PR template/labels,
  agent review rubric, multiple project-local agent skills in `.claude/skills/` or equivalent) or
  estimated first-pass acceptance is high, but the score maps to L1–L2: warn that agent usage may
  outpace merge safety; prioritize verification, types, and CI before raising autonomy.
- **Codebase ahead of practices** — Score maps to L3+ but collaboration infrastructure is absent
  and workflow artifacts are missing: warn that raising agent autonomy without shared context
  will increase iteration cycles; prioritize `AGENTS.md`, plans dir, and collaboration tracking.

Do not infer org-wide maturity levels — only repo-observable signals.
