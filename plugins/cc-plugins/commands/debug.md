---
description: "Debug and fix plugin issues. Checks directory structure, frontmatter syntax, manifest validity, and component files. Provides detailed error analysis with specific fix recommendations and examples."
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "Optional: path to plugin directory (default: current directory)"
model: "sonnet"
disable-model-invocation: false
---

# Debug Plugin

Debugs and fixes common plugin issues with detailed analysis and recommendations.

## Usage

```bash
/cc-plugins:debug
/cc-plugins:debug /path/to/plugin
/cc-plugins:debug ./my-plugin
```

## What It Does

1. **Checks Directory Structure**:
   - Verifies all required directories exist
   - Identifies missing or misplaced files
   - Reports structural issues

2. **Validates Manifest**:
   - Checks JSON validity
   - Verifies required fields
   - Detects format issues
   - Validates field types

3. **Inspects Components**:
   - Scans all markdown files
   - Validates YAML frontmatter
   - Checks for syntax errors
   - Reports missing metadata

4. **Analyzes Components**:
   - Tests commands independently
   - Validates agent definitions
   - Checks skill structure
   - Verifies scripts are executable

5. **Provides Fixes**:
   - Specific error messages
   - Code examples for fixes
   - Step-by-step instructions
   - Common issues database

## Output

### Success Output

```
✓ Plugin debug analysis complete

Plugin: my-awesome-plugin

Status: No issues found!

Directory Structure: ✓ PASSED
Manifest: ✓ PASSED
Components: ✓ PASSED

Summary: 0 issues, 0 warnings
```

### Issues Found Output

```
✗ Plugin debug found 4 issues:

┌─ CRITICAL ISSUES (must fix)
│
├─ 1. Missing manifest file
│   Location: .claude-plugin/plugin.json
│   Problem: Plugin manifest does not exist
│   Fix: Run /cc-plugins:create my-plugin
│
├─ 2. Invalid command frontmatter
│   Location: commands/invalid.md
│   Problem: Missing 'description' in YAML frontmatter
│   Fix: Add to frontmatter:
│        ---
│        description: "Your command description"
│        allowed-tools: ["Bash", "Read", "Write"]
│        ---
│
└─ 3. Malformed manifest JSON
│   Location: .claude-plugin/plugin.json
│   Problem: JSON syntax error on line 5
│   Hint: Check for missing commas or quotes

┌─ WARNINGS (should fix)
│
├─ 1. Missing tests directory
│   Location: tests/
│   Suggestion: Create tests/ directory and add test files
│
└─ 2. Missing README.md
    Location: README.md
    Suggestion: Run /cc-plugins:document to generate

Summary:
- Critical Issues: 3 (must fix before publishing)
- Warnings: 2 (recommended to fix)

Next Steps:
1. Fix critical issues first
2. Run /cc-plugins:validate to confirm fixes
3. Address warnings
4. Run /cc-plugins:debug again to verify
```

## Parameters

- **Path** ($1): Optional. Path to plugin directory (default: current directory)

## Common Issues & Fixes

### Issue 1: Invalid JSON in Manifest

**Error Message:**
```
Malformed manifest JSON
JSON Decode Error: Expecting value
```

**Fix:**
```bash
# Check JSON syntax
python3 -m json.tool .claude-plugin/plugin.json

# Common issues:
# 1. Missing comma after fields
# 2. Unclosed quotes
# 3. Trailing commas

# Example fix:
# WRONG: "name": "my-plugin" "version": "1.0.0"
# RIGHT: "name": "my-plugin", "version": "1.0.0"
```

### Issue 2: Missing Frontmatter in Command

**Error Message:**
```
Command frontmatter incomplete
Missing 'description' field in commands/my-cmd.md
```

**Fix:**
Add to top of `commands/my-cmd.md`:
```yaml
---
description: "What this command does"
allowed-tools: ["Bash", "Read", "Write"]
---
```

### Issue 3: Plugin Name Not Kebab-Case

**Error Message:**
```
Plugin name must be in kebab-case
Got: MyPlugin (invalid)
Expected: my-plugin (valid)
```

**Fix:**
```bash
# In .claude-plugin/plugin.json
# Change from:
"name": "MyPlugin"

# To:
"name": "my-plugin"
```

### Issue 4: Missing Required Fields

**Error Message:**
```
Manifest missing required field: version
```

**Fix:**
Add to `.claude-plugin/plugin.json`:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description"
}
```

### Issue 5: Script Not Executable

**Error Message:**
```
Script not executable: scripts/deploy.sh
```

**Fix:**
```bash
chmod +x scripts/deploy.sh
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

ISSUES=0
WARNINGS=0
CRITICAL=0

echo "Debugging plugin: $PLUGIN_DIR"
echo ""

# Check for manifest
MANIFEST_PATH="$PLUGIN_DIR/.claude-plugin/plugin.json"
if [ ! -f "$MANIFEST_PATH" ]; then
  echo "✗ CRITICAL: Missing manifest file"
  echo "   Location: $MANIFEST_PATH"
  echo "   Fix: Run /cc-plugins:create my-plugin"
  ((CRITICAL++))
  ((ISSUES++))
else
  # Check manifest validity
  if python3 -c "import json; json.load(open('$MANIFEST_PATH'))" 2>/dev/null; then
    echo "✓ Manifest file is valid JSON"
  else
    echo "✗ CRITICAL: Manifest contains invalid JSON"
    echo "   Location: $MANIFEST_PATH"
    echo "   Fix: Check JSON syntax (missing commas, quotes, etc.)"
    echo "   Help: python3 -m json.tool $MANIFEST_PATH"
    ((CRITICAL++))
    ((ISSUES++))
  fi
fi

echo ""
echo "Checking directory structure..."

# Check directories
for dir in commands agents skills; do
  if [ ! -d "$PLUGIN_DIR/$dir" ]; then
    echo "✗ WARNING: Missing $dir/ directory"
    ((WARNINGS++))
    ((ISSUES++))
  else
    echo "✓ $dir/ directory exists"
  fi
done

echo ""
echo "Checking components..."

# Check command files
if [ -d "$PLUGIN_DIR/commands" ]; then
  for cmd_file in "$PLUGIN_DIR/commands"/*.md; do
    if [ -f "$cmd_file" ]; then
      cmd_name=$(basename "$cmd_file")

      # Check for frontmatter
      if head -1 "$cmd_file" | grep -q "^---$"; then
        # Check for required frontmatter fields
        if grep -q "^description:" "$cmd_file"; then
          echo "✓ $cmd_name has valid frontmatter"
        else
          echo "✗ WARNING: $cmd_name missing 'description' in frontmatter"
          echo "   Fix: Add 'description: \"...\"' to YAML frontmatter"
          ((WARNINGS++))
          ((ISSUES++))
        fi

        if grep -q "^allowed-tools:" "$cmd_file"; then
          echo "✓ $cmd_name has allowed-tools defined"
        else
          echo "✗ WARNING: $cmd_name missing 'allowed-tools' in frontmatter"
          echo "   Fix: Add 'allowed-tools: [\"Bash\", \"Read\"]' to frontmatter"
          ((WARNINGS++))
          ((ISSUES++))
        fi
      else
        echo "✗ CRITICAL: $cmd_name missing frontmatter"
        echo "   Fix: Add at top of file:"
        echo "   ---"
        echo "   description: \"Command description\""
        echo "   allowed-tools: [\"Bash\"]"
        echo "   ---"
        ((CRITICAL++))
        ((ISSUES++))
      fi
    fi
  done
fi

echo ""
echo "Checking configuration files..."

# Check for README
if [ ! -f "$PLUGIN_DIR/README.md" ]; then
  echo "✗ WARNING: Missing README.md"
  echo "   Fix: Run /cc-plugins:document"
  ((WARNINGS++))
  ((ISSUES++))
else
  echo "✓ README.md exists"
fi

# Check for tests directory
if [ ! -d "$PLUGIN_DIR/tests" ]; then
  echo "✗ WARNING: Missing tests/ directory"
  echo "   Fix: mkdir -p tests/ and add test files"
  ((WARNINGS++))
  ((ISSUES++))
else
  echo "✓ tests/ directory exists"
fi

# Check for .gitignore
if [ ! -f "$PLUGIN_DIR/.gitignore" ]; then
  echo "✗ INFO: Missing .gitignore"
  echo "   Note: Recommended for version control"
  ((WARNINGS++))
else
  echo "✓ .gitignore exists"
fi

echo ""
echo "Summary:"
echo "--------"
echo "Critical Issues: $CRITICAL (MUST FIX)"
echo "Warnings:        $WARNINGS (RECOMMENDED)"
echo "Total Issues:    $ISSUES"

echo ""

if [ $CRITICAL -eq 0 ] && [ $ISSUES -eq 0 ]; then
  echo "✓ No issues found! Plugin is ready to use."
  exit 0
elif [ $CRITICAL -eq 0 ]; then
  echo "⚠ Plugin has warnings but should work. Consider fixing them."
  echo ""
  echo "Next steps:"
  echo "1. Review warnings above"
  echo "2. Apply recommended fixes"
  echo "3. Run /cc-plugins:debug again to verify"
  exit 0
else
  echo "✗ Plugin has critical issues that must be fixed."
  echo ""
  echo "Next steps:"
  echo "1. Fix critical issues (numbered above)"
  echo "2. Run /cc-plugins:debug again to verify"
  echo "3. Run /cc-plugins:validate to confirm"
  exit 1
fi
