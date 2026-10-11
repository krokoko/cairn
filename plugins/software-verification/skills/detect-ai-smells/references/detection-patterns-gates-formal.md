# Detection Patterns (Gates III — Formal Vacuity)

Continues `detection-patterns-gates.md`. AI011 and formal-spec gate patterns.

## AI011: Vacuous Formal Specs

| Gate type | Tools | What it catches |
|-----------|-------|-----------------|
| Anti-vacuity controls | Custom mutation runner invoking the supported checker | Relevant invariant violations not detected |
| Spec↔code sync gate | Generated TLA+ from FSM, diff check on regen | Model checks stale or incomplete transition table |
| Verified-marker enforcement | Script parsing `(verified=…)` + `implements_in` | Markers claiming proof with no linked artifact |
| Effective scanner rules | Inspect defaults/inheritance and known-secret control | No effective detection despite a green scan |
| Coverage scope validation | Coverage scoped to verified core crate/module | Green coverage on adapter code while core untested |
| Presence ⇒ mandatory meta-gate | Custom CI step | Formal artifact on disk but gate skipped silently |

**Vacuous-spec principle:** qualify a critical claim with a relevant known-bad control and a known-good
case. If a genuine violation passes, investigate configuration, reachability, and scope; do not
conclude the product is verified. Equivalent or out-of-scope mutations are not qualification failures.

**TLA+ anti-vacuity pattern** (conceptual — adapt per toolchain):

```toml
# Custom runner input, not a built-in TLC format; confirm this edit violates the reachable claim
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
meta-gates for active formal claims or required checks; document drafts and inactive examples.
