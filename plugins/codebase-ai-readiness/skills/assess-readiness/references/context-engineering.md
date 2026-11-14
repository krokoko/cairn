# Context Engineering Friendliness

## Definition

Context engineering friendliness measures how well a codebase's structure supports
the deliberate management of what an agent sees, in what sequence, and with what
priority. Inadequate context is one possible source of agent errors.

## Four dimensions

### 1. File size and granularity

Agents operate within finite context windows. Files that exceed agent working memory
force partial reads or require complex summarization strategies.

| Signal | Investigate | Useful evidence |
|--------|-------------|-----------------|
| File/function length outliers | Unrelated concerns or expensive partial reads | A representative task can find and understand the relevant behavior |
| Many small files | Excessive indirection or new dependency cycles | Boundaries support changes without unexpected edit spread |
| Cohesion | Concepts that change independently are entangled | A scoped change preserves unrelated behavior and dependency rules |

Exclude generated/vendor output when measuring. Counts locate investigation targets; a
shorter file is not proof of single responsibility or easier maintenance. Avoid splitting
cohesive code solely to meet a line threshold.

For repeatable triage, start with the three largest maintained source files per major component,
or the project's existing size rule. A 500-line warning can locate candidates; under 300 lines is
not automatically good. Trace a representative task through each candidate and record unrelated
concerns, navigation steps, unexpected edits, and new coupling. Recommend a split only when that
exercise shows a boundary problem; otherwise retain the file with the rationale.

### 2. Layered documentation for progressive loading

Agents should be able to load context progressively — from high-level overview to
implementation detail — without needing to read everything upfront.

| Layer | Purpose | Where it belongs |
|-------|---------|------------------|
| Entry point | What this project is, how to get started | Root `README.md` |
| Agent guide | Conventions, rules, tool usage | `CLAUDE.md`, `AGENTS.md` |
| Architecture | System structure, module relationships | `ARCHITECTURE.md`, `docs/adr/` |
| Module docs | Per-module purpose, API, and constraints | Per-directory `README.md` |
| Inline | Why (not what) for non-obvious decisions | Code comments, docstrings |

### 3. Navigability and entry points

Agents need clear, discoverable paths to find relevant code without loading the entire
repository into context.

| Signal | Good | Problematic |
|--------|------|-------------|
| Directory structure | Predictable, semantically organized | Flat or deeply nested with no logic |
| Entry points | Clearly marked (main, index, app) | Multiple ambiguous entry points |
| Cross-references | Docs link to code; code links to docs | Orphaned docs, no breadcrumbs |
| Module exports | Explicit public APIs (barrel files, `__init__.py`) | Everything public, no clear surface |

### 4. Retrieval-friendly organization

Agents use search (grep, glob, semantic) as primary navigation. The codebase should
be optimized for these access patterns.

| Signal | Good | Problematic |
|--------|------|-------------|
| Consistent naming | Same concept = same term everywhere | Synonyms (handler/controller/processor) |
| Structured headings | Markdown with clear hierarchy | Flat text without sections |
| Unique identifiers | Functions, types, files with distinctive names | Generic names (utils.ts, helpers.py, common.go) |
| Searchable patterns | Predictable file patterns per module | Ad-hoc organization |

## Scoring signals

### Strong context friendliness (score 76-100)
- Cohesive boundaries supported by navigation/change evidence
- Layered documentation from root to module level
- Clear entry points and module exports
- Consistent naming without synonyms
- Agent context file with progressive disclosure design
- Structured headings in all documentation
- Names let tasks find the relevant domain concept; established conventions are considered

### Moderate context friendliness (score 51-75)
- Generally navigable modules, with some demonstrated cohesion or indirection problems
- Root README and some module-level docs
- Entry points identifiable but not explicitly marked
- Mostly consistent naming with occasional drift
- Some agent context file present
- Documentation partially structured

### Weak context friendliness (score 26-50)
- Unrelated concerns or excessive indirection repeatedly obstruct scoped changes
- Only root README, no layered docs
- Entry points ambiguous
- Naming inconsistencies across modules
- No agent context file
- Documentation unstructured or missing headings

### Poor context friendliness (score 0-25)
- Important tasks require broad, poorly explained changes across the codebase
- No documentation beyond minimal README
- No clear entry points
- Inconsistent naming pervasive
- No agent context
- Flat or chaotic directory structure

## Key principle

> Reduce what the agent must process. Context engineering friendliness is codebase *affordances* for targeted information selection.
