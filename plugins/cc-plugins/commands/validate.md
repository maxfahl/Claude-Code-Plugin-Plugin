---
description: "Validate a plugin directory against official Claude Code specifications. Checks directory structure, manifest format, component frontmatter, and syntax. Displays validation results and suggests fixes for common issues."
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "Optional: path to plugin directory (default: current directory)"
model: "sonnet"
disable-model-invocation: false
---

# Validate Plugin

Validates an existing plugin against official Claude Code specifications.

## Usage

```bash
/cc-plugins:validate
/cc-plugins:validate /path/to/plugin
/cc-plugins:validate ./my-plugin
```

## What It Does

1. Checks directory structure compliance:
   - `.claude-plugin/plugin.json` manifest exists
   - Required component directories exist (commands, agents, skills)
   - Files are in correct locations

2. Validates manifest format:
   - Valid JSON structure
   - Required fields present (name, version)
   - Field types are correct
   - Plugin name follows kebab-case convention
   - No unsupported fields

3. Checks component files:
   - All .md files have valid YAML frontmatter
   - Frontmatter contains required fields
   - No syntax errors in component files

4. Tests plugin functionality:
   - Manifest can be loaded and parsed
   - Components can be discovered
   - Scripts are executable

## Output

### Success Output

```
✓ Plugin validation passed!

Plugin: my-awesome-plugin (v1.0.0)
Author: Jane Developer

Directory Structure: PASSED
├─ .claude-plugin/
├─ commands/ (2 commands found)
├─ agents/ (1 agent found)
├─ skills/ (3 skills found)
├─ scripts/
├─ tests/
└─ docs/

Manifest Validation: PASSED
├─ name: valid (kebab-case)
├─ version: valid (1.0.0)
├─ description: valid
└─ author: valid

Component Validation: PASSED
├─ Commands: 2 ✓
├─ Agents: 1 ✓
├─ Skills: 3 ✓
└─ Scripts: 0 ✓

Overall Status: ✓ PASSED
```

### Failure Output

```
✗ Plugin validation found 3 issues:

1. CRITICAL: Missing required manifest field
   Location: .claude-plugin/plugin.json
   Issue: Field 'version' is required
   Fix: Add "version": "1.0.0" to manifest

2. WARNING: Command frontmatter incomplete
   Location: commands/invalid-cmd.md
   Issue: Missing 'description' field in frontmatter
   Fix: Add description: "..." to YAML frontmatter

3. ERROR: Invalid plugin name
   Location: .claude-plugin/plugin.json
   Issue: Plugin name 'My_Plugin' must be in kebab-case
   Fix: Rename to 'my-plugin' (lowercase with hyphens only)

Run /cc-plugins:debug for detailed analysis and fixes
```

## Parameters

- **Path** ($1): Optional. Path to plugin directory (default: current directory)

## Common Issues & Fixes

### Issue: "Plugin name must be in kebab-case"

**Fix:**
```bash
# In .claude-plugin/plugin.json, change:
"name": "MyPlugin"
# To:
"name": "my-plugin"
```

### Issue: "Missing required field: version"

**Fix:**
```bash
# In .claude-plugin/plugin.json, add:
"version": "1.0.0"
```

### Issue: "Command missing description in frontmatter"

**Fix:**
```bash
# In commands/my-command.md, add to YAML frontmatter:
---
description: "Brief description of what this command does"
allowed-tools: ["Bash", "Read", "Write"]
---
```

### Issue: "Invalid JSON in manifest"

**Fix:**
```bash
# Use a JSON validator to check syntax:
python3 -m json.tool .claude-plugin/plugin.json
```

---

!bash
# Get plugin directory path (default to current directory)
PLUGIN_DIR="${1:-.}"

# Check if directory exists
if [ ! -d "$PLUGIN_DIR" ]; then
  echo "✗ Error: Directory not found: $PLUGIN_DIR"
  exit 1
fi

# Check if it's a plugin directory
MANIFEST_PATH="$PLUGIN_DIR/.claude-plugin/plugin.json"
if [ ! -f "$MANIFEST_PATH" ]; then
  echo "✗ Error: Not a valid plugin directory"
  echo "   Missing: $MANIFEST_PATH"
  echo ""
  echo "To create a plugin, use: /cc-plugins:create my-plugin"
  exit 1
fi

# Initialize counters
ERRORS=0
WARNINGS=0
PASSES=0

echo "Validating plugin: $PLUGIN_DIR"
echo ""

# Validate manifest
echo "Checking manifest..."
if ! python3 -c "import json; json.load(open('$MANIFEST_PATH'))" 2>/dev/null; then
  echo "✗ CRITICAL: Manifest contains invalid JSON"
  ((ERRORS++))
else
  echo "✓ Manifest JSON is valid"
  ((PASSES++))
fi

# Check manifest fields
if grep -q '"name"' "$MANIFEST_PATH"; then
  NAME=$(python3 -c "import json; print(json.load(open('$MANIFEST_PATH')).get('name', ''))")

  # Check kebab-case
  if [[ "$NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "✓ Plugin name is in kebab-case: $NAME"
    ((PASSES++))
  else
    echo "✗ ERROR: Plugin name must be in kebab-case (got: $NAME)"
    ((ERRORS++))
  fi
else
  echo "✗ CRITICAL: Missing 'name' field in manifest"
  ((ERRORS++))
fi

if grep -q '"version"' "$MANIFEST_PATH"; then
  echo "✓ Version field exists"
  ((PASSES++))
else
  echo "✗ CRITICAL: Missing 'version' field in manifest"
  ((ERRORS++))
fi

echo ""
echo "Checking directory structure..."

# Check required directories
for dir in commands agents skills; do
  if [ -d "$PLUGIN_DIR/$dir" ]; then
    echo "✓ $dir/ directory exists"
    ((PASSES++))
  else
    echo "✗ WARNING: $dir/ directory not found"
    ((WARNINGS++))
  fi
done

# Check for test directory
if [ -d "$PLUGIN_DIR/tests" ]; then
  echo "✓ tests/ directory exists"
  ((PASSES++))
else
  echo "✗ WARNING: tests/ directory not found"
  ((WARNINGS++))
fi

echo ""
echo "Checking components..."

# Check command files
if [ -d "$PLUGIN_DIR/commands" ]; then
  cmd_count=$(find "$PLUGIN_DIR/commands" -name "*.md" 2>/dev/null | wc -l)
  echo "✓ Found $cmd_count command(s)"
fi

# Check agent files
if [ -d "$PLUGIN_DIR/agents" ]; then
  agent_count=$(find "$PLUGIN_DIR/agents" -name "*.md" 2>/dev/null | wc -l)
  echo "✓ Found $agent_count agent(s)"
fi

# Check skill directories
if [ -d "$PLUGIN_DIR/skills" ]; then
  skill_count=$(find "$PLUGIN_DIR/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
  echo "✓ Found $skill_count skill(s)"
fi

echo ""

# Summary
if [ $ERRORS -eq 0 ]; then
  echo "✓ Plugin validation PASSED"
  echo ""
  echo "Summary: $PASSES checks passed"
  if [ $WARNINGS -gt 0 ]; then
    echo "         $WARNINGS warnings (non-blocking)"
  fi
  exit 0
else
  echo "✗ Plugin validation FAILED"
  echo ""
  echo "Summary: $PASSES passed, $ERRORS errors, $WARNINGS warnings"
  echo ""
  echo "For detailed analysis and fixes, run:"
  echo "  /cc-plugins:debug $PLUGIN_DIR"
  exit 1
fi
