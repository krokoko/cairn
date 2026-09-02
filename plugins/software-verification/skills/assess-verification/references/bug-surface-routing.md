# Bug-Surface Routing

Payoff from verification tracks the **hardest question a component must answer**, not how
many tools you run. Route expensive oracles to where the bug-surface is large; a deep stack on
a simple invariant is ceremony.

## Five bug-surface classes

| Class | Hardest question | Example domains | Typical latent bugs | Tool ROI |
|-------|------------------|-----------------|---------------------|----------|
| **A — Local invariant** | Does this single rule hold under concurrency? | Atomic counters, id generators, rate limiters | Rare if author uses correct primitives (Mutex, atomics) | Low for formal methods; lint + unit tests usually sufficient |
| **B — Arithmetic / conservation** | Do operations preserve totals, bounds, or invariants over integers? | Ledgers, inventory, quotas, billing | Overflow, silent wrap, plausible-but-wrong comments defending raw `+`/`-` | High for checked arithmetic, property tests, bounded proofs (Kani, Z3, CrossHair) |
| **C — Protocol / concurrency** | Does behavior hold across schedules, leader changes, partitions? | Consensus, distributed locks, workflow engines | Demo passes, cluster wedges after failover; §5.4.2-style commit rules missing | High — see C1–C4 subroutes below |
| **D — Untrusted input** | Does parsing/decoding stay total on arbitrary bytes? | Parsers, importers, API deserializers | Panics on edge bytes; underflow in hand-indexed parsers | High for fuzzing + sanitizers; property tests on round-trips |
| **E — Probabilistic / learned** | Is output quality within bounds over time? | ML models, ranking, LLM features | Semantic drift, no ground truth | Operational oracles: shadow, differential, statistical thresholds |

## Class C subroutes (C1–C4)

Class C is too coarse as a single bucket. Route by **what you are verifying**:

| Subtype | What you're verifying | Best approach | Examples |
|---------|----------------------|---------------|----------|
| **C1 — Local concurrency** | Threads/tasks and shared memory | Schedule exploration | Loom, Shuttle, Coyote |
| **C2 — Distributed implementation** | Real async/network code under failures | Deterministic simulation testing (DST) | Turmoil, MadSim |
| **C3 — Protocol/design** | Abstract states/messages/invariants | Model checking | P, Quint, TLA+, Apalache |
| **C4 — Black-box system** | Observable history/consistency | History verification + fault injection | Jepsen |

### Routing distinctions

| Tool family | Controls | Verifies |
|-------------|----------|----------|
| Loom / Shuttle | Scheduling of concurrent **implementation** code | Interleavings in real code |
| Turmoil / MadSim | Simulated network/filesystem + injected failures | Distributed **implementation** under failure |
| P / Quint / TLA+ | Abstract behavioral model | Protocol **design** correctness |
| Jepsen | Operations + failures on running system | **Observable history** consistency |

**Rule:** Pick the subroute matching the artifact you have (implementation code vs abstract spec vs
deployed system). C3 without C2 leaves an implementation gap; C2 without C3 leaves a design gap.

### Model ↔ implementation bridge

When both C3 spec and implementation exist, add **model-based conformance testing**:
Quint Connect, P test drivers, or custom trace adapters replay spec scenarios against implementation
state. See `verification-taxonomy.md`.

## Empirical anchor (harness ON vs OFF)

| Domain | Class | OFF latent bug | Harness role |
|--------|-------|----------------|--------------|
| Seat counter | A | None (Mutex + guard correct) | Overhead — proof/coverage insurance |
| Money ledger | B | Recipient `to + amount` u64 overflow; false "can't overflow" comment | Caught — `checked_add` + exhaustive proof |
| Raft KV | C | New leader never commits after failover | Indispensable — spec-first encoded §5.4.2 rule |

**Rule:** Class A → resist formal-method sprawl. Class B → prioritize arithmetic oracles.
Class C → formal spec + simulation are load-bearing, not optional.

## Classification signals

Use repo evidence to assign each component a primary class (secondary allowed):

| Signal | Suggests class |
|--------|----------------|
| Single mutex/atomic guarding one counter or slot | A |
| Money, balances, quantities, conservation language in specs | B |
| Leader election, replication, partition, quorum, FSM with many events | C (then pick C1–C4) |
| `async`/`await` + network I/O + retry logic in distributed service | C2 |
| `*.tla`, Quint/P modules, protocol docs without impl sim | C3 |
| Deployed service, consistency claims, multi-node | C4 |
| `parse_*`, decoders, bulk import, untrusted string/bytes input | D |
| Model inference, embeddings, scoring, non-deterministic output | E |

When signals conflict, classify by **worst plausible failure** (money loss → B even if also concurrent).

## Routing recommendations

| Class | Mandatory floor | Route expensive tools when |
|-------|-----------------|----------------------------|
| A | Types, lint, focused unit tests | Never by default; property tests only if law is easy to state |
| B | Checked arithmetic, property laws, BDD on acceptance criteria | Conservation or bounds are stated requirements |
| C | Executable spec, model check or DST, replay labels | Any leader/partition/retry semantics — use C1–C4 table |
| D | Fuzz target, panic-freedom, sanitizer on hot path | Parser or decoder on untrusted input |
| E | Metamorphic/differential + operational validation | Any learned or stochastic output |

## Report fields

For each component in the assessment, record:

- **Primary class** (A–E)
- **C subtype** (C1–C4) when class is C
- **Evidence** (files, spec language, failure modes)
- **Recommended depth** (floor / standard / deep)
- **Ceremony risk** — flag when **maturity tier 4+** formal-method tools exist on Class A with no gap
