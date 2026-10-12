# Verification Cost Tiers

Split verification by **wall-clock cost**, not only lifecycle stage (shift-left T1–T4). Agents need
cheap oracles on every edit and expensive oracles only where bug-surface warrants them. Load
`../../assess-verification/references/bug-surface-routing.md` for class A–E routing.

## Three cost tiers (check / verify-quick / verify-full)

Analogous to progressive hardening harnesses; map to your toolchain:

| Tier | When | Target latency | Purpose |
|------|------|----------------|---------|
| **Check** | Every save / post-tool-use hook | Seconds | Fail fast on style, types, meta-gates, traceability drift |
| **Verify-quick** | After logical unit / before commit | ~1–3 min | Behavior floor: unit + property tests, coverage, quick formal path |
| **Verify-full** | Before merge / release / large refactor | Minutes+ | Expensive instruments: mutation, fuzz campaigns, multi-seed simulation, TSAN |

Tiers are **orthogonal** to shift-left T1–T4: a check can run at T1 (post-write) or T3 (CI only).
Prefer T1 for Check tier so agents self-correct before accumulating debt.

## Default gate contents by ecosystem

Adapt names to the claim and stack; these are candidate contents, not a required bundle. Budget
timings are planning targets, not guarantees. Retain scope/completion evidence for each selected check.

### Check (~seconds)

- Formatter + linter (strict)
- Type checker
- Secret scan (qualified effective rules, including defaults)
- Meta-gates: traceability, spec↔code sync, requirement↔scenario coverage
- File-size / doc-count hygiene (if project enforces)

### Verify-quick (~minutes)

- Unit + integration tests (focused or affected-first; full suite at CI boundary)
- Property tests on pure core laws
- Line/branch coverage floor on verified core
- Quick formal path where routed (bounded model check, single-seed DST, TLC on small state space)
- Dependency/supply-chain advisory scans that block on advisories

### Verify-full (pre-merge / nightly)

- Mutation testing on verified core
- Fuzzing with persisted crash artifacts
- Multi-seed deterministic simulation / chaos replay
- Thread sanitizers / Loom on concurrent modules
- Full integration + E2E where not run in verify-quick

## Routing by bug-surface class

| Class | Check | Verify-quick | Verify-full |
|-------|-------|--------------|-------------|
| **A** (local invariant) | ✓ full | Unit + lint | Usually skip formal/sim |
| **B** (arithmetic) | ✓ full | Property tests + checked ops + BDD | Mutation; bounded proof if tractable |
| **C** (protocol) | ✓ full + spec sync | TLC/DST single seed, BDD | Multi-seed DST, Loom, TSAN |
| **D** (untrusted input) | ✓ full | Unit + property on valid grammar | Fuzz + sanitizers |
| **E** (probabilistic) | ✓ full | Contract/schema gates | Shadow/canary eval jobs (operational lane) |

## Routing by risk class

Cross-check bug-surface with product risk:

| Risk | Check | Verify-quick | Verify-full | Review consideration |
|------|-------|--------------|-------------|------------|
| Low | Local/CI feedback | Relevant local behavior | Justify if useful | Ambiguous intent |
| Medium | Local + CI | Boundary/behavior checks | Representative deeper cases | Unresolved meaning |
| High | Local + CI | Critical decisions | Fault/integration evidence where needed | Consequential decisions and existing policy |
| Critical | Local + CI | Qualified critical claims | Supported deeper methods with scoped completion | Applicable domain obligations |

A risk label does not mandate formal verification, signing, or a new approval. Select methods for
the actual failure surface; document why omitted checks are inapplicable and what would change that.

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Full suite only at verify-full | Move fmt/lint/types to Check at T1 |
| verify-full on every save | Split tiers; schedule heavier checks by scope, consequence, and measured cost |
| Check tier skips meta-gates | Add traceability and vacuity probes (see gate-design-patterns) |
| Same tier for all components | Per-component verify-full only where class or risk demands |

## Strategy deliverables

For each target component, specify:

1. **Check commands** — exact scripts/hooks (pre-commit, post-write)
2. **Verify-quick commands** — CI job or local alias
3. **Verify-full commands** — required check vs nightly
4. **Skip justification** — explicit inapplicability or approved exception, with remaining limits
5. **Evidence requirements** — source/oracle revisions, environment, completion, bounds, and retained artifacts
