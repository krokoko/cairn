# Detection Patterns (Gates III — Formal Vacuity)

Continues `detection-patterns-gates.md`. AI011 and formal-spec gate patterns.

## AI011: Vacuous Formal Specs

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Anti-vacuity mutation table | TLC `--mutate`, custom invariant probes | Invariants that pass when guard is flipped |
| Spec↔code sync gate | Generated TLA+ from FSM, diff check on regen | Model checks stale or incomplete transition table |
| Verified-marker enforcement | Script parsing `(verified=…)` + `implements_in` | Markers claiming proof with no linked artifact |
| Non-empty scanner rules | gitleaks/detect-secrets config lint | Secret scan that always passes |
| Coverage scope validation | Coverage scoped to verified core crate/module | Green coverage on adapter code while core untested |
| Presence ⇒ mandatory meta-gate | Custom CI step | Formal artifact on disk but gate skipped silently |

**Vacuous-spec principle:** a formal spec or gate config must fail when a **known-bad mutation** is
introduced. If the mutation passes, the gate manufactures confidence — worse than no gate.

**TLA+ anti-vacuity pattern** (conceptual — adapt per toolchain):

```toml
# mutations.toml — each invariant MUST fail when find is replaced with replace
[[mutations]]
find    = "(state = \"Archived\" => ~ ENABLED Next)"
replace = "(state = \"Archived\" => ENABLED Next)"
expect  = "ArchivedTerminal"
```

**Detection patterns:**
```bash
# Formal specs present
find . \( -name '*.tla' -o -name '*.cfg' -o -name 'mutations.toml' \) -not -path '*/vendor/*' 2>/dev/null

# Verified markers in requirements (heuristic — verify implements_in manually)
grep -rn '(verified=' docs/requirements spec/requirements 2>/dev/null

# Secret scanner with empty rules (config-dependent — inspect manually)
grep -Ern 'rules[[:space:]]*=[[:space:]]*\[\]' .gitleaks.toml .harness/config/gitleaks.toml 2>/dev/null
```

Load `../../design-strategy/references/gate-design-patterns.md` for presence⇒mandatory and vacuous-gate
anti-patterns. Add to minimum viable gate set (priority 10): anti-vacuity probes + presence⇒mandatory
meta-gates when formal specs or `(verified=…)` markers exist.
