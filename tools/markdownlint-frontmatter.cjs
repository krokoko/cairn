/**
 * Validates SKILL.md YAML frontmatter against skill-frontmatter.schema.json.
 */

"use strict";

const path = require("path");
const fs = require("fs");

function loadAllowedProperties() {
  const fallback = new Set([
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
  ]);

  try {
    const schemaPath = path.resolve(__dirname, "..", "schemas", "skill-frontmatter.schema.json");
    const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
    if (schema && schema.properties) {
      return new Set(Object.keys(schema.properties));
    }
  } catch {
    // use fallback
  }
  return fallback;
}

const ALLOWED_PROPERTIES = loadAllowedProperties();

function extractDescription(frontmatter) {
  // Capture the full block scalar: terminate at the next non-indented line (top-level key)
  // or true end of string. `$(?![\s\S])` matches only end-of-string, not end-of-line under /m,
  // so multi-line descriptions are captured in full (not truncated to the first line).
  const block = frontmatter.match(/^description:\s*\|\s*\n([\s\S]*?)(?=\n\S|$(?![\s\S]))/m);
  if (block) {
    return block[1].replace(/\n[ \t]+/g, " ").trim();
  }
  const single = frontmatter.match(/^description:\s*(.+)$/m);
  if (single) {
    return single[1].trim().replace(/^["']|["']$/g, "");
  }
  return "";
}

module.exports = {
  names: ["skill-frontmatter", "SKILL002"],
  description: "SKILL.md files must have valid frontmatter",
  tags: ["skill", "frontmatter"],
  parser: "none",
  function: function skillFrontmatter(params, onError) {
    if (!params.name.endsWith("SKILL.md")) {
      return;
    }

    const frontMatterLines = params.frontMatterLines || [];
    if (frontMatterLines.length === 0) {
      onError({
        lineNumber: 1,
        detail: "SKILL.md must have YAML frontmatter (---)",
        context: "Missing frontmatter",
      });
      return;
    }

    const frontmatter = frontMatterLines.filter((line) => line !== "---").join("\n");

    const nameMatch = frontmatter.match(/^name:\s*(.+)$/m);
    if (!nameMatch) {
      onError({
        lineNumber: 2,
        detail: 'Frontmatter must include "name" field',
        context: "Missing name",
      });
    } else {
      const name = nameMatch[1].trim().replace(/^["']|["']$/g, "");
      if (!/^[a-z][a-z0-9-]*$/.test(name)) {
        onError({
          lineNumber: 2,
          detail: `Skill name must be kebab-case: "${name}"`,
          context: "Invalid name format",
        });
      }
      const dirName = path.basename(path.dirname(params.name));
      if (name !== dirName) {
        onError({
          lineNumber: 2,
          detail: `Skill name "${name}" must match directory "${dirName}"`,
          context: "Name/directory mismatch",
        });
      }
    }

    const description = extractDescription(frontmatter);
    if (!description) {
      onError({
        lineNumber: 2,
        detail: 'Frontmatter must include "description" field',
        context: "Missing description",
      });
    } else if (description.length < 20) {
      onError({
        lineNumber: 2,
        detail: `Description must be at least 20 characters (current: ${description.length})`,
        context: "Description too short",
      });
    } else if (description.length > 1024) {
      onError({
        lineNumber: 2,
        detail: `Description exceeds 1024 characters (current: ${description.length})`,
        context: "Description too long",
      });
    }

    const topLevelKeys = frontmatter.match(/^[a-z][\w-]*(?=:)/gm) || [];
    for (const key of topLevelKeys) {
      if (!ALLOWED_PROPERTIES.has(key)) {
        onError({
          lineNumber: 2,
          detail: `Unknown frontmatter property: "${key}"`,
          context: "Unknown property",
        });
      }
    }
  },
};
