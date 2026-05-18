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

## Scoring signals

### Strong context friendliness (score 76-100)
- 90%+ of files under 300 lines
- Layered documentation from root to module level
- Clear entry points and module exports
- Consistent naming without synonyms
- Agent context file with progressive disclosure design
- Structured headings in all documentation
- No generic filenames (utils, helpers, misc, common)

### Moderate context friendliness (score 51-75)
- Most files under 500 lines, some outliers
- Root README and some module-level docs
- Entry points identifiable but not explicitly marked
- Mostly consistent naming with occasional drift
- Some agent context file present
- Documentation partially structured

### Weak context friendliness (score 26-50)
- Many files >500 lines, some >1000
- Only root README, no layered docs
- Entry points ambiguous
- Naming inconsistencies across modules
- No agent context file
- Documentation unstructured or missing headings

### Poor context friendliness (score 0-25)
- Files routinely >1000 lines
- No documentation beyond minimal README
- No clear entry points
- Inconsistent naming pervasive
- No agent context
- Flat or chaotic directory structure

## Key principle

> The cheapest optimization for agent performance is reducing what the agent must
> process to accomplish its task.

Context engineering friendliness is about codebase *affordances* — structural properties
that make it easy for agents to select the right slice of information without human
guidance.
