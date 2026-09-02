# Change Semantics

## Orthogonal to bug surface

Bug surfaces (A–E) answer: **What kind of bug is difficult here?**
Change modes answer: **What kind of change is being made?**

These axes are orthogonal. Route verification by **both**:

```text
final routing = f(bug_surface, change_mode, archetype, criticality)
```

Do not add a Bug Surface F — change mode is a separate dimension.

## Change modes

| Mode | Verification implication | Primary oracle |
|------|-------------------------|----------------|
| **Feature addition** | Validate new intended behavior | Exact, contract, property tests on new spec |
| **Bug fix** | Reproduce counterexample + regression | Failing test from bug report → permanent regression |
| **Behavior-preserving refactor** | Semantic equivalence | Differential oracle (old vs new on shared inputs) |
| **Framework/library migration** | Old version as reference oracle | Differential + contract compatibility |
| **Language port** | Semantic equivalence across languages | Differential + cross-language test vectors |
| **Compiler/generated transformation** | Translation validation / refinement | Alive2-style refinement check (output refines input) |
| **Data/schema migration** | Bidirectional properties + replay | Round-trip, replay against golden traces |
| **Performance optimization** | Equivalence + performance envelope | Differential correctness + benchmark oracle |
| **Agent policy/tool change** | Temporal / capability invariants | State-machine tests, tool-sequence contracts |

## Behavior-preserving changes

For refactors, migrations, and optimizations, verification is **dramatically easier** than
greenfield features — the old program is the specification:

```text
                    INPUT
                      │
              ┌───────┴────────┐
              ▼                ▼
          Old program      New program
              │                │
              └───────┬────────┘
                      ▼
            semantic comparison
                      │
                 ┌────┴─────┐
                 ▼          ▼
              equal      counterexample
```

### Translation validation

For compiler passes and automated transforms (not whole-program proof):

- Check that transformation **refines** the original (output behavior ≥ input behavior).
- Alive2 is the canonical LLVM example — validates a specific pass, not the entire compiler.
- Do not attempt to prove the whole transformer correct when refinement checking suffices.

## Routing matrix (examples)

| Change mode | Class B ledger | Class C distributed | Class D parser |
|-------------|----------------|---------------------|----------------|
| Feature addition | Property tests on new invariants | Model check new protocol rules | Fuzz new decode paths |
| Bug fix | Regression from counterexample | Replay failing trace | Fuzz input from crash |
| Refactor | Differential equivalence | DST replay + differential | Round-trip differential |
| Migration | Differential + replay | Quint Connect / trace replay | Fuzz + differential |
| Perf optimization | Equivalence + bounds | Equivalence + latency SLO | Equivalence + perf envelope |

## Classification signals

| Signal in task/PR | Likely change mode |
|-------------------|-------------------|
| "Rename", "extract", "move without behavior change" | Behavior-preserving refactor |
| "Upgrade X to Y", "migrate from A to B" | Framework/library migration |
| "Port to Rust/Go" | Language port |
| "Fix #123", reproducer attached | Bug fix |
| "Add endpoint/feature/field" | Feature addition |
| "Optimize", "reduce latency" | Performance optimization |
| "Change agent prompt/tool policy" | Agent policy/tool change |

When uncertain, assume the **hardest** applicable mode (feature addition > refactor).

## Integration with safe evolution

Load `safe-evolution.md`. Parallel Change (expand → migrate → contract) handles **shape**
changes incrementally; change semantics handles **what to verify** at each phase:

| Phase | Change mode | Verification |
|-------|-------------|--------------|
| Expand | Feature addition (new path) | New path tested; old path unchanged |
| Migrate | Refactor per caller | Differential: old entry = new entry per caller |
| Contract | Removal | No callers on old path; equivalence held throughout |

## Agent search implications

| Change mode | Search strategy |
|-------------|-----------------|
| Refactor / migration | Differential verifier is authoritative — strong fit for verifier-guided search |
| Feature addition | Spec + property tests; broader search space |
| Bug fix | Counterexample-guided refinement |
| Perf optimization | Mandatory equivalence + objective latency |

## Assessment fields

For each active change or component, record in strategy/report:

- **Primary change mode** (from table above)
- **Equivalence oracle available?** (yes/no — old version, reference impl, formal spec)
- **Recommended verification depth** given mode + bug surface
- **Ceremony risk** — deep formal stack on simple refactor without equivalence check
