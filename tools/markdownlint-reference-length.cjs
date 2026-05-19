/**
 * Validates reference markdown files stay under 100 lines.
 */

"use strict";

const MAX_LINES = 100;

module.exports = {
  names: ["reference-length", "REF001"],
  description: "Reference docs must be at most 100 lines",
  tags: ["reference", "length"],
  parser: "none",
  function: function referenceLength(params, onError) {
    if (!params.name.includes("/references/") || !params.name.endsWith(".md")) {
      return;
    }

    const totalLines = (params.frontMatterLines || []).length + params.lines.length;
    if (totalLines > MAX_LINES) {
      onError({
        lineNumber: 1,
        detail: `Reference file has ${totalLines} lines (max: ${MAX_LINES}). Split into another reference file.`,
        context: `${totalLines} lines`,
      });
    }
  },
};
