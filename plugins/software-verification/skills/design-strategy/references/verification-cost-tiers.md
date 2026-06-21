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

Adapt names to your stack; one tool per bug class within each tier.

### Check (~seconds)

- Formatter + linter (strict)
- Type checker
- Secret scan (non-empty ruleset)
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

| Risk | Check | Verify-quick | Verify-full | Human gate |
|------|-------|--------------|-------------|------------|
| Low | CI Check | CI verify-quick | Nightly optional | None |
| Medium | Hook + CI Check | CI verify-quick | Pre-merge sample | Agent review |
| High | Hook + CI Check | CI verify-quick | Required verify-full | Ship review |
| Critical | Hook + CI Check | CI verify-quick + attestation | Required verify-full + formal evidence | Domain expert |

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Full suite only at verify-full | Move fmt/lint/types to Check at T1 |
| verify-full on every save | Split tiers; route heavy tools by class C/D only |
| Check tier skips meta-gates | Add traceability and vacuity probes (see gate-design-patterns) |
| Same tier for all components | Per-component verify-full only where class or risk demands |

## Strategy deliverables

For each target component, specify:

1. **Check commands** — exact scripts/hooks (pre-commit, post-write)
2. **Verify-quick commands** — CI job or local alias
3. **Verify-full commands** — required check vs nightly
4. **Skip justification** — explicit opt-out when class A and risk Low (auditable, not silent)
