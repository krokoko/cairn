# Detection Patterns (Oracle Tampering — AI012)

Load `ai-smells-taxonomy.md` for AI012 definition. Distinct from AI010 (vacuous tests) and AI011
(vacuous formal specs).

## AI012: Oracle Tampering / Evaluator Gaming

| Gate type | Tools / mechanism | What it catches |
|-----------|-------------------|-----------------|
| Cross-artifact diff review | Custom CI script, `git diff` heuristics | Impl + test/spec/config changed together |
| Assertion-presence regression | Diff-aware lint | Assertions removed or weakened |
| Skip/xfail detection | pytest, Jest, cargo test lints | New skips without `oracle-change` label |
| Verifier config hash | CI compares config hash to baseline | Timeout/bound/iteration reductions |
| Coverage exclusion audit | diff-cover, custom grep | New `# pragma: no cover`, `.coveragerc` exclusions |
| Sanitizer flag check | Build script assertion | ASan/UBSan/TSan disabled in same PR as impl |
| Holdout access control | Repo permissions, separate holdout repo | Agent PR touches holdout scenario files |
| Snapshot review gate | `--ci` snapshot mode, required reviewer | Unreviewed snapshot churn |
| Property diff lint | Custom on property test files | Weakened preconditions/postconditions |
| Mandatory oracle-change label | Branch protection + bot | Impl+oracle PR without explicit review |

## Legitimate oracle evolution vs tampering

Tests and specs *should* change when requirements change. "Impl + oracle changed together" is a
triage signal, not a verdict. Decide with the direction of the change and its provenance:

| Signal | Legitimate evolution | Tampering suspect |
|--------|---------------------|-------------------|
| Direction | Oracle **strengthened** or extended (new cases, tighter bound) | Oracle **weakened** (bound loosened, case removed, skip added) |
| Provenance | Linked requirement change (REQ-ID updated, spec hash bumped with changelog) | No requirement change; only the implementation "needed" it |
| Authorship | Oracle change reviewed by someone other than the implementation author/agent | Same agent session changes both |
| Net effect | Mutation score / property count same or higher | Fewer assertions, lower kill rate, smaller explored state space |
| Failing test | Fixed by changing code; test kept | Fixed by changing the test |

**Decision rule:** weakening direction **and** no linked requirement change ⇒ block as AI012. Weakening
with a linked requirement change ⇒ require a human approver who is not the author; the `oracle-change`
label alone is not sufficient. Strengthening ⇒ allow.

## Detection heuristics (PR diff)

These greps triage; they do not decide. Feed matches into the table above.

```bash
# Files changed in same PR
IMPL=$(git diff --name-only origin/main... | grep -E '^src/|^lib/' | wc -l)
ORACLE=$(git diff --name-only origin/main... | grep -E 'test|spec|\.tla|\.quint|\.p$|pytest\.ini|jest\.config' | wc -l)
if [[ "$IMPL" -gt 0 && "$ORACLE" -gt 0 ]]; then
  gh pr view --json labels -q '.labels[].name' | grep -qx 'oracle-change' \
    || { echo 'AI012: impl + oracle changed without oracle-change label'; exit 1; }
fi

# Weakening signals in diff (fail build on High/Critical paths if any match)
git diff origin/main... -- '*.py' '*.rs' '*.ts' | grep -E '^\-.*assert|^\-.*expect\(|^\+.*skip|^\+.*xfail'
git diff origin/main... -- '*fuzz*' '*kani*' '*config*' | grep -E 'iterations|timeout|depth|bound'
```

**Coverage level:**
- **Full**: CI classifies direction (weakened vs strengthened) and blocks weakening without a linked requirement change and independent approver
- **Partial**: Warning on cross-artifact changes; manual review required
- **None**: No detection

## Link to oracle integrity

When AI012 fires, rate affected oracle `integrity: blocked` until human re-approves the property.
See `../../design-strategy/references/oracle-integrity.md`.

## Minimum viable gate set addition

Add to the minimum viable gate set (after AI011 anti-vacuity probes):

1. Cross-artifact diff gate for impl + test/spec/evaluator changes on High/Critical paths (AI012)
