# Oracle Integrity

## Why integrity matters

Oracle **strength** asks: "Is this oracle discriminating?"
Oracle **integrity** asks: "Can the agent undermine the oracle?"

A strong oracle the search agent can weaken is worse than a weak oracle everyone knows is weak.
At L4/L5 autonomy, integrity is a **hard prerequisite** — agent-mutable oracles do not count.

## Oracle Integrity Card

For each oracle on a critical path, evaluate seven dimensions:

| Dimension | Question | Values |
|-----------|----------|--------|
| **Authority** | Where did the property originate? | `approved-spec`, `mined-hypothesis`, `agent-generated`, `unknown` |
| **Independence** | Produced independently from implementation? | `high`, `medium`, `low` |
| **Mutability** | Can the implementation/search agent modify it? | `false` (required for L5), `true` |
| **Scope** | Coverage breadth | `exhaustive-model`, `bounded`, `sampled`, `statistical` |
| **Freshness** | Still represents current requirements? | `current`, `stale`, `unknown` |
| **Reproducibility** | Another process can rerun it? | `true`, `false` |
| **Provenance** | Traceable to requirement? | REQ-ID, spec hash, or `none` |
| **Generalization** | Covers classes of behavior or only examples? | `class`, `instance`, `none` |

### Compact integrity rating

For report tables, collapse to three levels:

| Rating | Criteria | Autonomy impact |
|--------|----------|-----------------|
| **Sound** | `agent_mutable=false`, `authority=approved-spec`, `independence=high`, `freshness=current` | Eligible for L4/L5 |
| **Degraded** | One dimension weak (e.g. sampled scope, medium independence) | Caps at L3–L4 |
| **Blocked** | `agent_mutable=true`, or `authority=agent-generated`, or `freshness=stale` | Not safe for autonomous search |

Full cards are required for High/Critical components and L4/L5 candidates.

## Example card

```yaml
oracle:
  type: temporal
  authority: approved-spec
  independence: high
  agent_mutable: false
  scope: exhaustive-model
  provenance: REQ-PAY-042
  freshness: current
  reproducible: true
  generalization: class
  integrity: sound
```

## Tampering patterns

Agents under search pressure may weaken evaluation without making tests vacuous (AI010):

| Tampering | Example | Detection signal |
|-----------|---------|-------------------|
| Assertion weakened | `balance >= 0` → `balance >= -100` | Property diff in PR |
| Test skipped | `pytest -k "not failing_test"` | Skip/xfail added |
| Bound reduced | `model_check_depth=100` → `10` | Config change + impl change |
| Iteration lowered | `fuzz_iterations=100000` → `100` | Verifier config diff |
| Tolerance widened | `abs(a-b) < 0.01` → `< 1.0` | Snapshot/tolerance diff |
| Precondition strengthened | `requires valid_input` → `requires false` | Property made easier to satisfy |
| Coverage excluded | `# pragma: no cover` on hot path | Coverage config change |
| Sanitizer disabled | `-fsanitize=address` removed | Build flag diff |
| Holdout exposed | Agent gains access to holdout scenarios | Access control change |
| Reference modified | Old version changed during migration | Differential oracle invalidated |

Load `../../detect-ai-smells/references/ai-smells-taxonomy.md` (AI012) for the smell taxonomy.
Coordinated `implementation + test/spec/evaluator` changes are the primary indicator.

## Protecting oracle integrity

| Control | Purpose |
|---------|---------|
| **Immutable spec pack** | Requirements, holdout tests, formal spec outside agent write scope |
| **Separate PR lanes** | Implementation PR cannot modify approved spec without human gate |
| **Config hash in CI** | Verifier bounds pinned; change requires explicit review |
| **Holdout isolation** | Behavioral twin scenarios in separate repo/secret |
| **Provenance tags** | `(verified=kani)` links to proof obligation, not just marker |
| **Anti-tampering gate** | Fail PR when impl + oracle files change together without `oracle-change` label |

## Mined invariants

Invariants from specification mining (Daikon, trace analysis) default to:

- `authority: mined-hypothesis`
- `agent_mutable: false` (once human-approved and promoted)
- `integrity: degraded` until human validates against requirements

**A mined invariant is a hypothesis, not a specification** until approved.

## Assessment checklist

For each component oracle:

1. Rate strength (strong/weak/none) — see `../../assess-verification/references/verification-taxonomy.md`
2. Rate integrity (sound/degraded/blocked) — this document
3. Flag oracle rot separately — passes but no longer asserts the right thing
4. For L5 candidates: require at least one **sound** oracle on every critical path
5. Flag AI012 indicators when impl + evaluator change in same agent session

## Related patterns

- `oracle-patterns.md` — oracle type selection
- `verifier-guided-search.md` — verifier must be integrity-protected
- `candidate-selection-policy.md` — mandatory properties use sound oracles
- `specification-mining.md` — bootstrapping oracles in brownfield systems
