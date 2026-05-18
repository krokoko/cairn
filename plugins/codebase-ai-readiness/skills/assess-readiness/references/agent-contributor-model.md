# Agent Contributor Model

## Core framing

AI agents are not just tools -- they are contributors to onboard. An AI-ready codebase
optimizes for **constrained decision-making**, **explicit intent**, and **fast,
machine-readable feedback**.

## The litmus test

> If an AI agent cloned this repo with no prior context, how long before it could
> safely make a small change?

If the answer is "never" or "only after a human explains things," the codebase is not
AI ready.

## Three governing principles

| Principle | Meaning | Agent failure when missing |
|-----------|---------|---------------------------|
| Minimize ambiguity | One obvious way to do things; no synonyms | Agent modifies the wrong abstraction |
| Maximize discoverability | Layered docs, clear entry points, predictable paths | Agent avoids changes or hallucinates intent |
| Encode intent explicitly | Comments explain why, contracts enforce shape | Agent breaks unrelated functionality |

## Mechanisms over intentions

Good intentions don't work; mechanisms do. Rules, hooks, and CI gates enforce habits
that humans might skip. Key mechanisms:

- **Rules/AGENTS.md**: Reusable, context-aware guidance loaded automatically
- **Hooks**: Pre-commit/post-tool scripts that block bad patterns deterministically
- **CI gates**: Required checks that produce binary pass/fail the agent can act on
- **Templates**: Issue and PR templates that enforce structured information

## Why a better AI won't fix an opaque codebase

The bottleneck is the codebase, not the model. When the repo is opaque, ambiguous, or
inconsistent, every agent will guess, stumble, and produce wrong or brittle changes.
Agents amplify existing patterns -- poor code quality doesn't just persist, it
accelerates. Without clean foundations, you automate the production of technical debt.

## What agents need vs what humans cope with

| Humans cope with | Agents need instead |
|------------------|---------------------|
| Experience and intuition | Explicit signals and discoverable structure |
| Slack messages and tribal knowledge | Versioned, co-located documentation |
| "We just know" | Machine-readable contracts and types |
| Loose rules, manual checks | Strict, fast, deterministic quality gates |
| Tolerance for ambiguity | One canonical way to operate |

## The verifiable abstraction standard

From verification research: an abstraction is only as useful as its testability. A
**verifiable abstraction** is an interface whose critical properties can be checked
automatically, cheaply enough to sit inside an iterative development loop. The measure
of an abstraction is not just its elegance -- it is its machine-checkability.

**Caveat**: Assurance is always relative to a property, a model, a specification, and a
trusted toolchain. Proving the wrong property is still the wrong system.
