/**
 * Cross-reference validation for Cairn marketplaces and plugin manifests.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const CLAUDE_MARKETPLACE_PATH = ".claude-plugin/marketplace.json";
const CODEX_MARKETPLACE_PATH = ".agents/plugins/marketplace.json";
const PLUGINS_ROOT = "plugins";

const BASE_DIR = path.resolve(process.cwd(), PLUGINS_ROOT);
const validationErrors = [];
const validationWarnings = [];

function resolvePathUnderBase(relativePath) {
  if (!relativePath || typeof relativePath !== "string") return null;
  const normalized = path.normalize(relativePath.replace(/^\.\//, "").replace(/\/$/, ""));
  if (normalized.startsWith("..") || path.isAbsolute(normalized)) return null;
  const fullPath = path.resolve(process.cwd(), normalized);
  const baseDir = path.resolve(BASE_DIR);
  // Use path.relative so sibling dirs like "plugins-evil" don't pass a bare startsWith("plugins") check.
  const rel = path.relative(baseDir, fullPath);
  if (rel !== "" && (rel.startsWith("..") || path.isAbsolute(rel))) return null;
  return fullPath;
}

function error(message) {
  validationErrors.push(message);
  console.error(`ERROR: ${message}`);
}

function warn(message) {
  validationWarnings.push(message);
  console.warn(`WARNING: ${message}`);
}

function validateMarketplace(marketplacePath, manifestPathParts) {
  if (!fs.existsSync(marketplacePath)) {
    error(`Marketplace file not found: ${marketplacePath}`);
    return;
  }

  let marketplace;
  try {
    marketplace = JSON.parse(fs.readFileSync(marketplacePath, "utf8"));
  } catch (e) {
    error(`Failed to parse ${marketplacePath}: ${e.message}`);
    return;
  }

  if (!Array.isArray(marketplace.plugins)) {
    error(`${marketplacePath} must have a "plugins" array`);
    return;
  }

  for (const plugin of marketplace.plugins) {
    validatePlugin(plugin, marketplacePath, manifestPathParts);
  }
}

function validatePlugin(plugin, marketplacePath, manifestPathParts) {
  const pluginName = plugin?.name;
  if (!pluginName) {
    error(`Plugin entry missing "name" in ${marketplacePath}`);
    return;
  }

  const source =
    typeof plugin.source === "string"
      ? plugin.source
      : plugin.source?.path || `${PLUGINS_ROOT}/${pluginName}`;
  const pluginDir = resolvePathUnderBase(source);
  if (!pluginDir) {
    error(`Invalid plugin path for "${pluginName}": ${source}`);
    return;
  }

  if (!fs.existsSync(pluginDir)) {
    error(`Plugin directory not found: ${pluginDir}`);
    return;
  }

  if (fs.lstatSync(pluginDir).isSymbolicLink()) {
    error(`Plugin directory cannot be a symlink: ${pluginDir}`);
    return;
  }

  if (path.basename(pluginDir) !== pluginName) {
    error(`Directory "${path.basename(pluginDir)}" does not match plugin name "${pluginName}"`);
  }

  const pluginJsonPath = path.join(pluginDir, ...manifestPathParts);
  if (!fs.existsSync(pluginJsonPath)) {
    error(`Manifest not found: ${pluginJsonPath}`);
    return;
  }

  const pluginJson = JSON.parse(fs.readFileSync(pluginJsonPath, "utf8"));
  if (pluginJson.name !== pluginName) {
    error(`Name mismatch for "${pluginName}" in ${pluginJsonPath}`);
  }

  const skillsDir = path.join(pluginDir, "skills");
  if (!fs.existsSync(skillsDir)) {
    warn(`Plugin "${pluginName}" has no skills/ directory`);
  }
}

console.log("=== Cross-Reference Validation ===\n");
validateMarketplace(CLAUDE_MARKETPLACE_PATH, [".claude-plugin", "plugin.json"]);
validateMarketplace(CODEX_MARKETPLACE_PATH, [".codex-plugin", "plugin.json"]);

console.log("\n=== Summary ===");
console.log(`Errors: ${validationErrors.length}`);
console.log(`Warnings: ${validationWarnings.length}`);

if (validationErrors.length > 0) {
  process.exit(1);
}
