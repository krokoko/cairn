# Context Engineering Friendliness

## Definition

Context engineering friendliness measures how well a codebase's structure supports
the deliberate management of what an agent sees, in what sequence, and with what
priority. Agent failures typically stem from inadequate context rather than model
incapability.

## Four dimensions

### 1. File size and granularity

Agents operate within finite context windows. Files that exceed agent working memory
force partial reads or require complex summarization strategies.

| Signal | Good | Problematic |
|--------|------|-------------|
| Average file length | <300 lines | >500 lines |
| Maximum file length | <800 lines | >2000 lines |
| Function length | <50 lines | >100 lines |
| Single-responsibility | One concept per file | Multiple unrelated concerns |

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

## Pass profiles

The denominator for this category is the **Context engineering friendliness** table in
`category-definitions-agent.md`. Decide PASS or FAIL per row with these profiles:

| Signal | PASS when | FAIL when |
|--------|-----------|-----------|
| File size distribution | 90%+ of source files under 300 lines and none over 2000 (measured, see the skill's Step 1) | Many files over 500 lines |
| Layered documentation | Root README, architecture doc, and module-level docs all exist and link downward | Only a root README |
| Clear entry points | Entry files identifiable; public API exported explicitly | Ambiguous entry points; everything public |
| Retrieval-friendly naming | No generic filenames (utils, helpers, misc, common); one term per concept | Generic names or synonyms common |
| Structured headings | Docs use a heading hierarchy | Flat text |

## Key principle

> Reduce what the agent must process. Context engineering friendliness is codebase *affordances* for targeted information selection.
