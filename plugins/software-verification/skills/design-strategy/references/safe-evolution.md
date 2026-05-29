# Safe Evolution Strategy

How agents should make breaking or large-scale changes **safely** — incrementally and reversibly —
instead of the risky one-shot diff an agent reaches for by default. Two complementary patterns:
**Parallel Change** for interface/shape changes, **Sweep** for applying one rule across many files.

## Parallel Change (expand → migrate → contract)

Agents asked to rename or reshape something tend to edit the definition and every caller in a single
diff — exactly the big-bang change that creates a breaking window and is hard to review or revert.
Parallel change separates the *shape change* from the *caller changes* into three independently
shippable, reversible phases:

| Phase | Action | Property |
|-------|--------|----------|
| Expand | Add the new form alongside the old; both coexist and produce identical results | Nothing breaks yet; old callers untouched |
| Migrate | Move callers from old to new, incrementally, at their own pace | Each migration is small and independently verifiable |
| Contract | Remove the old form once nothing depends on it | Drift eliminated; surface is clean again |

Use it for: public API/interface changes, renames touching many callers, schema/data migrations,
config-shape changes, and any change crossing teams, services, or versions you do not control.
The old form stays operational through the migration window, so there is no breaking window at all.

## Sweep (one rule, many files, disciplined batches)

Apply a single rule uniformly across many files in disciplined batches, so the codebase moves from
old convention to new without drift or dangling exceptions. Three execution modes by precision:

| Mode | When | Caveat |
|------|------|--------|
| Regex search-and-replace | Trivial textual changes (headers, URLs) | Syntactically blind — never for structural edits |
| Codemod (AST-based) | Structural transforms: renames, API migrations | Precise and repeatable; preferred default |
| Agentic sweep | Edits needing judgment: legitimate exceptions, related docs, local context | Reasoning per file; must still be gated |

### Sweep safeguards (required)

1. Write the rule down explicitly before executing.
2. Sample 3-4 candidate sites manually first to validate the rule.
3. Execute in small, reviewable batches with checkpoints — not one giant diff.
4. Gate each batch on passing tests **and** a diff review.
5. Verify test coverage actually exercises the changed behavior (a green suite that never runs the
   swept paths proves nothing — see the happy-path and oracle-strength concerns).

## Why this matters for autonomy

Big-bang agent edits are the dangerous failure mode: a single huge diff is hard to review, hard to
revert, and turns one wrong assumption into a repo-wide regression. Staged evolution keeps every step
small, independently verifiable, and reversible — which is what lets the verification pipeline (not a
human reading a massive diff) remain the authoritative gate.
