# Development Guide

This guide explains how to create, validate, and test plugins for the autonomy-rails marketplace.

## Prerequisites

- [mise](https://mise.jdx.dev/) for task running and tool management
- Python 3.10+ with `jsonschema` package (for validation scripts): `pip install jsonschema`
- Bash (for hook scripts and linting)

Install mise-managed tools:

```bash
mise install
```

## Creating a new plugin

### 1. Create the directory structure

```bash
mkdir -p plugins/my-plugin/.claude-plugin
mkdir -p plugins/my-plugin/hooks
mkdir -p plugins/my-plugin/scripts
mkdir -p plugins/my-plugin/skills/my-skill/references
```

### 2. Write the plugin manifest

Create `plugins/my-plugin/.claude-plugin/plugin.json`:

```json
{
  "$schema": "../../../schemas/plugin.schema.json",
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "What this plugin does in one sentence",
  "author": "Your Name",
  "keywords": ["keyword1", "keyword2"],
  "license": "Apache-2.0"
}
```

### 3. Write your first skill

Create `plugins/my-plugin/skills/my-skill/SKILL.md` with YAML frontmatter and a step-by-step workflow. See `docs/DESIGN_GUIDELINES.md` for authoring rules.

### 4. Add reference documents

Create `plugins/my-plugin/skills/my-skill/references/*.md` for domain knowledge. Keep each file under 100 lines.

### 5. Add hooks (optional)

If your skill produces a structured output file, add a PostToolUse hook to validate it. See `docs/DESIGN_GUIDELINES.md` for hook format.

### 6. Register in the marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "path": "plugins/my-plugin",
  "version": "0.1.0",
  "description": "What this plugin does",
  "keywords": ["keyword1", "keyword2"]
}
```

## Running validation locally

Run all checks:

```bash
mise run check
```

This runs:
- **lint**: JSON validity, kebab-case names, SKILL.md frontmatter, line limits, marketplace consistency
- **validate**: JSON Schema validation of all manifests

Run checks individually:

```bash
mise run lint
mise run validate
```

## Testing a plugin with Claude Code

1. Install the plugin in Claude Code using the plugin marketplace
2. Invoke each skill using its trigger phrases
3. Verify that:
   - The agent follows the workflow steps in order
   - Reference documents are loaded when needed
   - The output matches the specified format
   - Hooks fire and validate the output correctly

## Code style

- JSON: 2-space indentation
- Markdown: ATX headings, one sentence per line in prose
- Shell scripts: `set -euo pipefail`, quote variables, use `$()` over backticks
