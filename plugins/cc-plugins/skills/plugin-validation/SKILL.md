---
name: "plugin-validation"
description: "Expert validation of Claude Code plugins against official specifications. Activate for validating plugins, checking plugin errors, fixing specification violations, debugging plugin issues, verifying plugin structure, checking frontmatter syntax, or ensuring standards compliance. Uses validation scripts and provides clear fix instructions."
allowed-tools: ["Read", "Bash", "Grep", "Glob"]
version: "1.0.0"
---

# Plugin Validation Skill

Comprehensive validation of Claude Code plugins against official Anthropic specifications, with detailed error reporting and fix guidance.

## Overview

This skill provides expert knowledge for:
- Validating plugin structure and compliance
- Checking manifest and component syntax
- Identifying specification violations
- Providing actionable fix instructions
- Ensuring best practices compliance
- Debugging plugin issues

## When to Activate

This skill activates when you need to:
- Validate a Claude Code plugin
- Check for specification violations
- Debug why a plugin isn't working
- Verify plugin structure is correct
- Fix validation errors
- Ensure frontmatter is valid
- Check naming conventions
- Validate component files
- Ensure plugin meets standards
- Troubleshoot plugin loading issues

## Validation Scope

### What Gets Validated

1. **Plugin Manifest** (`.claude-plugin/plugin.json`)
   - Valid JSON syntax
   - Required fields present
   - Field value formats
   - Naming conventions

2. **Directory Structure**
   - Required directories exist
   - Proper organization
   - No extraneous files

3. **Commands** (`commands/*.md`)
   - Valid YAML frontmatter
   - Required fields present
   - Tool names valid
   - Proper formatting

4. **Agents** (`agents/*.md`)
   - Valid YAML frontmatter
   - Description within limits
   - Activation triggers present
   - Tool declarations valid

5. **Skills** (`skills/*/SKILL.md`)
   - Directory name matches skill name
   - Valid YAML frontmatter
   - Required fields present
   - Description within limits

6. **Hooks** (`hooks/*.md`) (if present)
   - Valid frontmatter
   - Event types valid
   - Patterns correctly formatted

## Validation Levels

### Critical (Must Fix)

Issues that prevent plugin from working:
- Invalid JSON in manifest
- Missing required manifest fields
- Invalid YAML frontmatter
- Missing frontmatter delimiters
- Invalid tool names
- Skill name mismatches
- Syntax errors

### Warnings (Should Fix)

Issues that may cause problems:
- Description too long (>1024 chars)
- Missing recommended fields
- Inconsistent naming
- Missing documentation
- No tests directory
- Incomplete frontmatter

### Info (Nice to Have)

Suggestions for improvement:
- Additional documentation
- More examples
- Better organization
- Enhanced descriptions

## Validation Process

### Step 1: Manifest Validation

Check `.claude-plugin/plugin.json`:

```bash
# Test JSON validity
python -m json.tool .claude-plugin/plugin.json > /dev/null

# Check required fields
jq -e '.name, .version, .description' .claude-plugin/plugin.json
```

**Required Fields**:
- `name` - Must be kebab-case
- `version` - Must be semantic version (e.g., "1.0.0")
- `description` - Brief description string

**Validation Rules**:
- Valid JSON syntax (no trailing commas)
- Name uses kebab-case: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Version format: `^\d+\.\d+\.\d+$`
- Description is non-empty string

### Step 2: Structure Validation

Check directory structure:

```bash
# Required directory
[ -d ".claude-plugin" ] || echo "ERROR: Missing .claude-plugin/"

# At least one component type
[ -d "commands" ] || [ -d "agents" ] || [ -d "skills" ] || \
  echo "WARNING: No component directories found"
```

**Required**:
- `.claude-plugin/` directory with `plugin.json`

**Expected** (at least one):
- `commands/` - For slash commands
- `agents/` - For specialized agents
- `skills/` - For reusable skills

**Optional**:
- `hooks/` - Event hooks
- `scripts/` - Utility scripts
- `docs/` - Documentation
- `tests/` - Test suite

### Step 3: Component Validation

#### Commands Validation

For each file in `commands/*.md`:

```bash
# Check frontmatter exists
head -1 "$file" | grep -q "^---$" || echo "ERROR: Missing frontmatter"

# Check description field
grep -q "^description:" "$file" || echo "ERROR: Missing description"

# Check tools are valid
grep "allowed-tools:" "$file" | grep -E "(Read|Write|Edit|Bash|Grep|Glob|WebFetch)"
```

**Requirements**:
- File starts with `---`
- Valid YAML frontmatter
- `description` field present
- Frontmatter closes with `---`
- Tool names valid (if present)

**Common Issues**:
- Missing frontmatter delimiters
- Invalid YAML syntax
- Unquoted strings with special chars
- Invalid tool names
- Missing description

#### Agents Validation

For each file in `agents/*.md`:

```bash
# Check frontmatter
head -1 "$file" | grep -q "^---$"

# Check description
grep -q "^description:" "$file"

# Check description length
desc_length=$(grep "^description:" "$file" | cut -d'"' -f2 | wc -c)
[ "$desc_length" -le 1024 ] || echo "ERROR: Description too long"
```

**Requirements**:
- Valid YAML frontmatter
- `description` field present
- Description max 1024 characters
- Description includes activation triggers
- Tool names valid (if specified)

**Common Issues**:
- Description exceeds 1024 chars
- Missing activation triggers
- Invalid tool names
- Malformed YAML

#### Skills Validation

For each directory in `skills/*/`:

```bash
# Check SKILL.md exists
[ -f "$skill_dir/SKILL.md" ] || echo "ERROR: Missing SKILL.md"

# Check name matches directory
skill_name=$(basename "$skill_dir")
grep -q "^name: \"$skill_name\"" "$skill_dir/SKILL.md" || \
  echo "ERROR: Name mismatch"

# Check description length
desc_length=$(grep "^description:" "$skill_dir/SKILL.md" | cut -d'"' -f2 | wc -c)
[ "$desc_length" -le 1024 ] || echo "ERROR: Description too long"
```

**Requirements**:
- `SKILL.md` file exists in skill directory
- `name` field matches directory name exactly
- `description` field present
- Description max 1024 characters
- Valid YAML frontmatter

**Common Issues**:
- Name doesn't match directory
- Missing SKILL.md file
- Description too long
- Invalid frontmatter

### Step 4: Syntax Validation

#### YAML Frontmatter

Common YAML errors:

```yaml
# ERROR: Unquoted string with colon
---
description: Command does: X and Y
---

# CORRECT
---
description: "Command does: X and Y"
---

# ERROR: Invalid array syntax
---
tools: [Read Write Bash]
---

# CORRECT
---
tools: ["Read", "Write", "Bash"]
---

# ERROR: Missing closing quote
---
description: "My description
---

# CORRECT
---
description: "My description"
---
```

#### JSON Manifest

Common JSON errors:

```json
// ERROR: Trailing comma
{
  "name": "my-plugin",
  "version": "1.0.0",
}

// CORRECT
{
  "name": "my-plugin",
  "version": "1.0.0"
}

// ERROR: Single quotes
{
  'name': 'my-plugin'
}

// CORRECT
{
  "name": "my-plugin"
}

// ERROR: Comments (not allowed in JSON)
{
  // This is my plugin
  "name": "my-plugin"
}

// CORRECT (no comments)
{
  "name": "my-plugin"
}
```

## Validation Tools

### Manual Validation

```bash
# Validate JSON
python -m json.tool .claude-plugin/plugin.json

# Check YAML (requires PyYAML)
python -c "import yaml; yaml.safe_load(open('file.md').read().split('---')[1])"

# Check naming
echo "plugin-name" | grep -E "^[a-z0-9]+(-[a-z0-9]+)*$"

# Find missing descriptions
grep -L "description:" agents/*.md
```

### Automated Validation

If using cc-plugins:

```bash
# Validate entire plugin
/cc-plugins:validate

# Validate specific plugin
/cc-plugins:validate /path/to/plugin

# Debug plugin issues
/cc-plugins:debug
```

## Error Categories

### Syntax Errors

**JSON Syntax Error**
```
Error: Invalid JSON in .claude-plugin/plugin.json
Line 8: unexpected character ',' (trailing comma)
```

**Fix**: Remove trailing commas from JSON

**YAML Syntax Error**
```
Error: YAML parsing failed in agents/helper.md
Line 3: unexpected character
```

**Fix**: Quote strings with special characters, check indentation

### Schema Errors

**Missing Required Field**
```
Error: Missing required field 'description' in commands/create.md
```

**Fix**: Add description field to frontmatter

**Invalid Field Value**
```
Error: Plugin name 'MyPlugin' must be kebab-case
Expected: my-plugin
```

**Fix**: Use lowercase with hyphens

### Format Errors

**Description Too Long**
```
Error: Description exceeds 1024 character limit in agents/analyzer.md
Current: 1156 characters
Limit: 1024 characters
```

**Fix**: Condense description, focus on triggers

**Invalid Tool Name**
```
Error: Invalid tool 'WriteFile' in commands/generate.md
Valid tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
```

**Fix**: Use correct tool name: "Write"

### Structure Errors

**Missing Directory**
```
Error: Required directory .claude-plugin/ not found
```

**Fix**: Create `.claude-plugin/` directory with `plugin.json`

**Skill Name Mismatch**
```
Error: Skill name 'dev-tools' doesn't match directory 'development-tools'
Location: skills/development-tools/SKILL.md
```

**Fix**: Update name in SKILL.md to match directory name

## Validation Report Format

Standard validation report structure:

```
🔍 PLUGIN VALIDATION REPORT
Plugin: my-plugin (v1.0.0)
Location: /path/to/plugin

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRITICAL ERRORS (2)

1. Invalid Manifest JSON
   File: .claude-plugin/plugin.json
   Line: 8
   Issue: Trailing comma after "description"
   Fix: Remove comma on line 8

2. Missing Frontmatter
   File: commands/create.md
   Issue: No YAML frontmatter found
   Fix: Add frontmatter at start of file

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  WARNINGS (1)

1. Description Length
   File: agents/helper.md
   Current: 1088 characters
   Limit: 1024 characters
   Suggestion: Condense by 64 characters

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ℹ️  INFO (2)

1. Missing Tests
   Suggestion: Add tests/ directory

2. No README
   Suggestion: Add README.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PASSED CHECKS (15)

✓ Plugin name uses kebab-case
✓ Version follows semantic versioning
✓ Commands have descriptions
✓ Agents have descriptions
✓ Skills names match directories
✓ Tool names are valid
✓ Directory structure present
[... more checks ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY
Critical: 2 (MUST FIX)
Warnings: 1 (RECOMMENDED)
Info: 2 (OPTIONAL)
Passed: 15

Status: ❌ FAILED (critical errors present)

🎯 NEXT STEPS
1. Fix critical errors (required for plugin to work)
2. Address warnings (recommended)
3. Re-run validation: /cc-plugins:validate
```

## Best Practices

### Validate Early and Often

- Validate after creating plugin structure
- Validate after adding each component
- Validate before committing changes
- Validate before publishing

### Fix Critical First

Priority order:
1. **Critical**: Must fix for plugin to work
2. **Warnings**: Should fix to avoid issues
3. **Info**: Nice to have improvements

### Use Validation Tools

- Automated validation scripts
- JSON/YAML linters
- Specification checkers
- Unit tests for validation

### Test After Fixes

After fixing validation errors:
1. Re-run validation
2. Restart Claude Code
3. Test plugin functionality
4. Verify components load

## Common Validation Workflows

### New Plugin Validation

```bash
# 1. Create plugin
/cc-plugins:create my-plugin

# 2. Add components
# ... create commands, agents, skills ...

# 3. Validate
/cc-plugins:validate my-plugin

# 4. Fix any errors
# ... make corrections ...

# 5. Re-validate
/cc-plugins:validate my-plugin

# 6. Test in Claude Code
# Restart Claude Code and test
```

### Existing Plugin Validation

```bash
# 1. Navigate to plugin
cd ~/.claude/plugins/my-plugin

# 2. Run validation
/cc-plugins:validate

# 3. Review report
# Check critical errors and warnings

# 4. Fix issues one by one
# Make corrections based on report

# 5. Re-validate after each fix
/cc-plugins:validate

# 6. Verify all checks pass
# Continue until no critical errors
```

### Pre-Publish Validation

```bash
# Complete checklist before publishing
/cc-plugins:validate --strict

# Ensure:
# ✓ All critical errors fixed
# ✓ All warnings addressed
# ✓ Tests passing
# ✓ Documentation complete
# ✓ Examples working
```

## Resources

See supporting documentation:
- `common-errors.md` - Detailed error catalog with fixes
- `spec-reference.md` - Quick specification reference

## Quick Reference

### Validation Checklist

**Manifest**:
- [ ] Valid JSON syntax
- [ ] Required fields present (name, version, description)
- [ ] Name is kebab-case
- [ ] Version is semantic (X.Y.Z)

**Structure**:
- [ ] `.claude-plugin/` directory exists
- [ ] At least one component directory present
- [ ] Plugin.json in correct location

**Commands**:
- [ ] Valid YAML frontmatter
- [ ] Description field present
- [ ] Tool names valid
- [ ] Frontmatter properly closed

**Agents**:
- [ ] Valid YAML frontmatter
- [ ] Description under 1024 chars
- [ ] Activation triggers included
- [ ] Tool names valid

**Skills**:
- [ ] SKILL.md exists
- [ ] Name matches directory
- [ ] Description under 1024 chars
- [ ] Valid YAML frontmatter

### Quick Validation Commands

```bash
# Validate JSON
python -m json.tool .claude-plugin/plugin.json > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"

# Check frontmatter
for f in commands/*.md; do head -1 "$f" | grep -q "^---$" && echo "✓ $f" || echo "✗ $f"; done

# Find long descriptions
for f in agents/*.md; do len=$(grep "^description:" "$f" | cut -d'"' -f2 | wc -c); [ "$len" -gt 1024 ] && echo "✗ $f ($len chars)"; done

# Check skill names
for d in skills/*/; do name=$(basename "$d"); grep -q "^name: \"$name\"" "$d/SKILL.md" && echo "✓ $name" || echo "✗ $name"; done
```

---

*Use this skill when validating Claude Code plugins to ensure compliance with official specifications and catch issues early.*
