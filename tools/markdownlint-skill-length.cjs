/**
 * Validates SKILL.md length limits (autonomy-rails design guidelines).
 * Max 300 lines (error). Warn at 250 lines.
 */

"use strict";

const MAX_LINES = 300;
const WARNING_LINES = 250;
const MAX_WORDS = 5000;
const WARNING_WORDS = 4000;

module.exports = {
  names: ["skill-length", "SKILL001"],
  description: "SKILL.md files should stay within autonomy-rails size limits",
  tags: ["skill", "length"],
  parser: "none",
  function: function skillLength(params, onError) {
    if (!params.name.endsWith("SKILL.md")) {
      return;
    }

    const frontMatterLines = params.frontMatterLines || [];
    const totalLines = frontMatterLines.length + params.lines.length;
    const content = params.lines.join("\n");
    const wordCount = content.split(/\s+/).filter(Boolean).length;

    if (totalLines > MAX_LINES) {
      onError({
        lineNumber: 1,
        detail: `Line count: ${totalLines} (max: ${MAX_LINES}). Move content to references/.`,
        context: `${totalLines} lines`,
      });
    } else if (totalLines > WARNING_LINES) {
      onError({
        lineNumber: 1,
        detail: `Line count: ${totalLines} (recommended: <${WARNING_LINES}). Consider moving content to references/.`,
        context: `${totalLines} lines (warning)`,
      });
    }

    if (wordCount > MAX_WORDS) {
      onError({
        lineNumber: 1,
        detail: `Word count: ${wordCount} (max: ${MAX_WORDS}). Move content to references/.`,
        context: `${wordCount} words`,
      });
    } else if (wordCount > WARNING_WORDS) {
      onError({
        lineNumber: 1,
        detail: `Word count: ${wordCount} (recommended: <${WARNING_WORDS}). Consider moving content to references/.`,
        context: `${wordCount} words (warning)`,
      });
    }
  },
};
