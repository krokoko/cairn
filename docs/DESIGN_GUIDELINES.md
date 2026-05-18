# Design Guidelines

This document describes how to design plugins for the autonomy-rails marketplace.

## Plugin philosophy

Plugins are **declarative**. They consist of JSON manifests, Markdown skill definitions, shell scripts for hooks, and Markdown reference documents. There is no compilation step. The AI agent (Claude Code, Codex, Cursor) reads the skill instructions and uses its own capabilities to execute them.

A plugin packages **domain expertise** into a form that AI agents can consume. The skill tells the agent _what to do_ and _how to do it_; the reference documents provide the _knowledge_ the agent needs to make good decisions.

## Anatomy of a plugin

```
plugins/<plugin-name>/
  .claude-plugin/
    plugin.json               # Manifest: name, version, description, author, keywords, license
  hooks/
    hooks.json                # PostToolUse hook definitions
  scripts/
    *.sh                      # Shell scripts invoked by hooks
  skills/
    <skill-name>/
      SKILL.md                # Skill definition (YAML frontmatter + Markdown body)
      references/
        *.md                  # On-demand reference documents
  README.md                   # Plugin documentation
```

## Plugin manifest (`plugin.json`)

- `name`: Required. Kebab-case identifier (`^[a-z][a-z0-9-]*$`), max 64 characters.
- `version`: Semantic version (e.g., `0.1.0`).
- `description`: Max 500 characters. Explain what the plugin does in one sentence.
- `author`: Name of the author.
- `keywords`: Array of search terms.
- `license`: SPDX identifier (e.g., `Apache-2.0`).

## SKILL.md authoring rules

### Size limits

- **SKILL.md**: Maximum 300 lines. If your skill needs more, split it into multiple skills or move knowledge into reference documents.
- **Reference documents**: Maximum 100 lines each. Keep them focused on one topic.

### YAML frontmatter

Every SKILL.md must start with YAML frontmatter between `---` delimiters:

```yaml
---
name: my-skill-name
description: |
  What this skill does and when to invoke it. Include trigger phrases
  that users or agents might use: "assess readiness", "check my codebase"
argument-hint: "[optional-arg-description]"
allowed-tools: Read Bash Glob Grep
user-invocable: true
---
```

Required fields: `name`, `description`.

### Markdown body

The body should contain:

1. **Context**: One paragraph explaining what the skill produces and why.
2. **Workflow**: Numbered steps the agent should follow. Be specific about what tools to use, what to look for, and what to output.
3. **Output format**: Describe the expected output structure (sections, tables, scores).
4. **References**: Point to `references/*.md` files for domain knowledge the agent should load.

### Writing effective instructions

- Write for an agent, not a human. Be explicit about what to search for, what patterns to match, what tools to use.
- Use imperative language: "Search for", "Read", "Calculate", "Write".
- Include concrete examples of patterns the agent should look for (file names, config keys, directory structures).
- Specify the output format precisely (section headings, table columns, score ranges).

## Reference documents

Reference documents contain domain knowledge that skills need. They are loaded on-demand by the agent when the skill references them.

- One topic per file. Don't combine scoring rubrics with tool catalogs.
- Use tables for structured data (scoring criteria, tool comparisons, decision matrices).
- Keep content actionable: the agent should be able to directly apply what it reads.
- Avoid narrative. Prefer structured formats: tables, lists, decision trees.

## Hooks

Hooks are shell scripts that run after the agent performs certain actions (e.g., writing a file). They validate output and provide feedback.

### Design principles

- **PostToolUse only**: Hooks fire after the agent uses a tool (Write, Edit).
- **Validation, not generation**: Hooks check that output meets structural requirements. They do not generate content.
- **Fast and idempotent**: Hooks should complete in seconds. They should produce the same result if run multiple times.
- **Graceful degradation**: If a dependency is missing, warn but do not fail with a confusing error.
- **JSON feedback**: Hook scripts output JSON with a `systemMessage` field that gets fed back to the agent.

### hooks.json format

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Naming conventions

- Plugin names: kebab-case (`codebase-ai-readiness`)
- Skill names: kebab-case, must match directory name (`assess-readiness`)
- Script files: kebab-case (`validate-report.sh`)
- Reference files: kebab-case (`scoring-rubric.md`)

## Self-contained plugins

Each plugin must be fully self-contained. Do not reference files from other plugins. If two plugins share a concept (e.g., autonomy levels), duplicate the relevant content compactly in each plugin's reference documents.
