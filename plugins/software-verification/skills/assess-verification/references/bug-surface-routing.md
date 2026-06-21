# Bug-Surface Routing

Payoff from verification tracks the **hardest question a component must answer**, not how
many tools you run. Route expensive oracles to where the bug-surface is large; a deep stack on
a simple invariant is ceremony.

## Five bug-surface classes

| Class | Hardest question | Example domains | Typical latent bugs | Tool ROI |
|-------|------------------|-----------------|---------------------|----------|
| **A — Local invariant** | Does this single rule hold under concurrency? | Atomic counters, id generators, rate limiters | Rare if author uses correct primitives (Mutex, atomics) | Low for formal methods; lint + unit tests usually sufficient |
| **B — Arithmetic / conservation** | Do operations preserve totals, bounds, or invariants over integers? | Ledgers, inventory, quotas, billing | Overflow, silent wrap, plausible-but-wrong comments defending raw `+`/`-` | High for checked arithmetic, property tests, bounded proofs (Kani, Z3) |
| **C — Protocol / concurrency** | Does behavior hold across schedules, leader changes, partitions? | Consensus, distributed locks, workflow engines | Demo passes, cluster wedges after failover; §5.4.2-style commit rules missing | High for TLA+/TLC, DST, Loom, schedule exploration |
| **D — Untrusted input** | Does parsing/decoding stay total on arbitrary bytes? | Parsers, importers, API deserializers | Panics on edge bytes; underflow in hand-indexed parsers | High for fuzzing + sanitizers; property tests on round-trips |
| **E — Probabilistic / learned** | Is output quality within bounds over time? | ML models, ranking, LLM features | Semantic drift, no ground truth | Operational oracles: shadow, differential, statistical thresholds |

## Empirical anchor (harness ON vs OFF)

Same domain built twice — bare toolchain vs full verification harness:

| Domain | Class | OFF latent bug | Harness role |
|--------|-------|----------------|--------------|
| Seat counter | A | None (Mutex + guard correct) | Overhead — proof/coverage insurance |
| Money ledger | B | Recipient `to + amount` u64 overflow; false "can't overflow" comment | Caught — `checked_add` + exhaustive proof |
| Raft KV | C | New leader never commits after failover | Indispensable — spec-first encoded §5.4.2 rule |

**Rule:** Class A → resist formal-method sprawl. Class B → prioritize arithmetic oracles. Class C →
formal spec + simulation are load-bearing, not optional.

## Classification signals

Use repo evidence to assign each component a primary class (secondary allowed):

| Signal | Suggests class |
|--------|----------------|
| Single mutex/atomic guarding one counter or slot | A |
| Money, balances, quantities, conservation language in specs | B |
| Leader election, replication, partition, quorum, FSM with many events | C |
| `parse_*`, decoders, bulk import, untrusted string/bytes input | D |
| Model inference, embeddings, scoring, non-deterministic output | E |

When signals conflict, classify by **worst plausible failure** (money loss → B even if also concurrent).

## Routing recommendations

| Class | Mandatory floor | Route expensive tools when |
|-------|-----------------|----------------------------|
| A | Types, lint, focused unit tests | Never by default; add property tests only if law is easy to state |
| B | Checked arithmetic, property laws, BDD on acceptance criteria | Conservation or bounds are stated requirements |
| C | Executable spec, model check or DST, replay labels | Any leader/partition/retry semantics |
| D | Fuzz target, panic-freedom, sanitizer on hot path | Parser or decoder on untrusted input |
| E | Metamorphic/differential + operational validation | Any learned or stochastic output |

## Report fields

For each component in the assessment, record:

- **Primary class** (A–E)
- **Evidence** (files, spec language, failure modes)
- **Recommended depth** (floor / standard / deep)
- **Ceremony risk** — flag when **maturity tier 4+** formal-method tools are present on Class A with no identified gap
