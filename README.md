<div align="center">
  <img alt="Cairn" width="250" src="docs/imgs/cairn.png" />

  <br />
  <br />

  <strong>
    From AI-assisted to autonomous: make your codebase ready for AI coding agents
  </strong>
  <br />
  <br />

  <a href="./LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" /></a>
  <img alt="Works with Claude Code, Cursor, Codex" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Cursor%20%7C%20Codex-8A2BE2" />
</div>

**Cairn** is an open-source toolkit of AI agent plugins that measure and improve how ready your codebase is for autonomous AI coding agents — charting a path from AI-assisted coding to verified, end-to-end autonomy.

> A *cairn* is a stack of stones that marks the trail on a climb — each one confirming how far you've come and pointing the way to the next. This project does the same for your codebase's journey to autonomy: marking where you stand today and the path to the next level.

## Why

AI coding agents can now generate code faster than humans can review it. The bottleneck has shifted from writing code to **trusting it**: can an agent change this codebase safely, without a human reading every line? Most codebases were built for human workflows (implicit knowledge, inconsistent tests, fragile CI, unclear ownership, and little machine-readable intent) and agents amplify those weaknesses at machine speed.

Cairn treats autonomy as something you **measure and earn**, not switch on. Install the plugins in any AI assistant that supports the plugin standard (Claude Code, Cursor, Codex), run a skill, and get back concrete, committable reports.

## What you get

- 📊 **AI readiness score & autonomy maturity map** — where your codebase sits on a 0–5 autonomy scale, a category breakdown, and the blockers holding you at your current level.
- 🗺️ **Prioritized improvement roadmap** — specific, effort-ranked actions to reach the next level.
- 🔬 **Verification strategy** — per-component oracles, missing tests, and what to verify to unlock safe autonomous iteration.
- 🚦 **AI-smell detection gates** — whether your CI catches the failure patterns AI-generated code tends to introduce.
- 🔗 **Requirement traceability** — proof that every change traces back to an intent, so agents don't silently drift from what was asked.

**Who it's for:** engineering teams adopting AI coding agents who want a measurable, incremental path to autonomy — not a leap of faith.

## Getting started

### Installation

Install the plugins in your AI agent:

**Claude Code:**

Add the marketplace

```bash
/plugin marketplace add krokoko/cairn
```

Add the plugins

```bash
/plugin install codebase-ai-readiness@cairn
/plugin install software-verification@cairn
```

**Codex:**

1. Clone this repository locally.
2. Open the repo in Codex so it discovers `.agents/plugins/marketplace.json`.
3. Restart Codex, open the plugin directory, choose the **Cairn** marketplace, and install a plugin.

Claude-specific PostToolUse hooks are not wired into Codex manifests; skills and references work the same.

**Cursor:**

Install plugins from a marketplace that indexes this repo, or copy skills into your project's agent configuration per Cursor's plugin documentation.

### Usage

Once installed, use the skills via slash commands in your AI agent:

```text
/assess-readiness              # Assess codebase AI readiness
/generate-roadmap              # Generate improvement roadmap
/assess-verification           # Assess verification maturity
/design-strategy               # Design verification strategy
/detect-ai-smells              # Assess AI smell detection gates
```

### Recommended workflow

For a full autonomy readiness pass on a codebase:

1. `/assess-readiness` → `readiness-report.md`
2. `/generate-roadmap` → `readiness-roadmap.md`
3. `/assess-verification` → `verification-report.md`
4. `/design-strategy` → `verification-strategy.md`
5. `/detect-ai-smells` → `ai-smells-gates-report.md`

Or use natural language triggers:

- "How AI-friendly is this codebase?"
- "What should I improve for AI readiness?"
- "What verification do I need?"
- "Design a verification strategy for this module"

## Levels of autonomy

We consider the following levels of autonomy:

| Level | Meaning |
| ----- | ------- |
| L0 | **Human only.** AI can explain code but should not modify it. |
| L1 | **Assisted.** Humans own design and implementation; AI suggests or drafts fragments. Changes are verified mainly by the author; little machine-readable intent or agent-safe structure. |
| L2 | **Reviewed.** Agents may touch the codebase in limited ways, but meaningful changes expect explicit human review before merge. CI exists but may be flaky or incomplete relative to risk. |
| L3 | **Bounded iteration.** Agents can iterate inside clear guardrails (e.g. scoped tasks, green tests, typed boundaries) with selective human review on higher-risk surfaces. Verification is stronger but not exhaustive. |
| L4 | **Verified autonomy.** Automated checks (tests, types, lint, policy, environments) are the primary gate; humans focus on intent, architecture, and exceptions. Most routine changes can ship when the verification stack passes. |
| L5 | **End-to-end autonomous.** Machine-readable requirements and strong oracles cover the system so agents can plan, implement, and validate work across the stack with confidence comparable to a mature human team on routine evolution—humans set goals and govern edge cases. |

## Available plugins

### Layer 1: diagnose

These plugins assess current readiness and provide recommendations to move to the next level of autonomy

#### Codebase AI readiness plugin

This plugin helps to answer the following question: "how AI friendly is my codebase, and what can I do to unlock more autonomy ?"

Most companies are not ready for autonomous coding. Their codebases often lack clear structure, consistent docs, testable boundaries, reliable CI, strong typing, deterministic environments and deployment, and explicit architecture decisions.

This plugin reviews an existing codebase and produces an autonomy maturity map.

The output includes a numeric score, a category breakdown of the findings, a recommended autonomy level, and the list of blockers for moving towards the next level of autonomy along with a roadmap of recommended actions.

#### Software verification plugin

This plugin helps to answer the following question: "given this codebase, these components, and these risks, what is the verification strategy that would unlock more autonomy ?".

The output is a maturity of the current verification strategy, breakdown of components in the codebase with a recommended verification path for each one of them, missing oracles, insights on where exact correctness is possible, where only statistical/empirical validation is realistic, recommendations on which components require human review, which parts are candidate for autonomous agent iteration.

## Contributing

Big shout out to our awesome contributors! Thank you for making this project better!

Contributions of all kinds are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Developer guide

If you want to add a new plugin to the library, check out our [design guidelines](./docs/DESIGN_GUIDELINES.md) and [development guide](./docs/DEVELOPMENT_GUIDE.md).

## License

This project is licensed under the [Apache-2.0 License](./LICENSE).
