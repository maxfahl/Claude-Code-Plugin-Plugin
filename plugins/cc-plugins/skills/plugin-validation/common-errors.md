# Common Plugin Validation Errors

Comprehensive catalog of common Claude Code plugin errors with detailed explanations and fixes.

## Table of Contents

1. [Manifest Errors](#manifest-errors)
2. [Frontmatter Errors](#frontmatter-errors)
3. [Structure Errors](#structure-errors)
4. [Naming Errors](#naming-errors)
5. [Tool Errors](#tool-errors)
6. [Length Limit Errors](#length-limit-errors)
7. [Syntax Errors](#syntax-errors)

---

## Manifest Errors

### E001: Invalid JSON Syntax

**Error Message**:
```
Error: Invalid JSON in .claude-plugin/plugin.json
JSONDecodeError: Expecting ',' delimiter: line 8 column 3 (char 156)
```

**Cause**: JSON syntax error (trailing comma, missing quotes, etc.)

**Example (Wrong)**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My plugin",
}
```

**Fix**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My plugin"
}
```

**Prevention**:
- Use a JSON validator/linter
- No trailing commas in JSON
- Use double quotes only
- Validate with: `python -m json.tool plugin.json`

---

### E002: Missing Required Field

**Error Message**:
```
Error: Missing required field 'name' in plugin.json
Required fields: name, version, description
```

**Cause**: Manifest missing a required field

**Example (Wrong)**:
```json
{
  "version": "1.0.0",
  "description": "My plugin"
}
```

**Fix**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My plugin"
}
```

**Required Fields**:
- `name` - Plugin name (kebab-case)
- `version` - Semantic version
- `description` - Brief description

---

### E003: Invalid Plugin Name Format

**Error Message**:
```
Error: Plugin name 'MyAwesomePlugin' must be in kebab-case
Expected format: my-awesome-plugin
Pattern: ^[a-z0-9]+(-[a-z0-9]+)*$
```

**Cause**: Plugin name not in kebab-case format

**Examples (Wrong)**:
```json
{"name": "MyPlugin"}          // CamelCase
{"name": "my_plugin"}         // snake_case
{"name": "My Plugin"}         // Spaces
{"name": "my.plugin"}         // Dots
{"name": "MY-PLUGIN"}         // Uppercase
```

**Fix**:
```json
{"name": "my-plugin"}         // Correct kebab-case
{"name": "my-awesome-plugin"} // Multiple words
{"name": "api-helper"}        // Lowercase only
```

**Rules**:
- All lowercase letters
- Numbers allowed
- Hyphens to separate words
- No spaces, underscores, or dots
- No leading/trailing hyphens

---

### E004: Invalid Version Format

**Error Message**:
```
Error: Invalid version '1.0' in plugin.json
Expected semantic version: MAJOR.MINOR.PATCH (e.g., 1.0.0)
```

**Cause**: Version doesn't follow semantic versioning

**Examples (Wrong)**:
```json
{"version": "1.0"}        // Missing patch
{"version": "v1.0.0"}     // Has 'v' prefix
{"version": "1"}          // Only major
{"version": "1.0.0.1"}    // Too many parts
```

**Fix**:
```json
{"version": "1.0.0"}      // Correct format
{"version": "2.3.1"}      // With updates
```

**Rules**:
- Format: `MAJOR.MINOR.PATCH`
- All three numbers required
- No prefix (no 'v')
- Only numbers and dots

---

### E005: Empty Description

**Error Message**:
```
Error: Empty description in plugin.json
Description must be a non-empty string
```

**Cause**: Description field is empty or missing

**Example (Wrong)**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": ""
}
```

**Fix**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A helpful plugin for developers"
}
```

---

## Frontmatter Errors

### E101: Missing Frontmatter Delimiter

**Error Message**:
```
Error: No frontmatter found in commands/create.md
Expected '---' delimiter at start of file
```

**Cause**: File doesn't start with `---` or missing closing `---`

**Example (Wrong)**:
```markdown
# My Command

Some content here.
```

**Fix**:
```markdown
---
description: "My command description"
---

# My Command

Some content here.
```

**Rules**:
- File must start with `---` (first line)
- Frontmatter must end with `---`
- No content before opening `---`

---

### E102: Invalid YAML Syntax

**Error Message**:
```
Error: YAML parsing failed in agents/helper.md
Line 3: mapping values are not allowed here
```

**Cause**: Invalid YAML syntax in frontmatter

**Example (Wrong)**:
```yaml
---
description: Command does: X and Y
tools: [Read Write]
---
```

**Fix**:
```yaml
---
description: "Command does: X and Y"  # Quote strings with colons
tools: ["Read", "Write"]              # Quote array elements
---
```

**Common Issues**:
- Unquoted strings with special characters (`:`, `&`, `*`, `#`, etc.)
- Invalid array syntax (missing quotes/commas)
- Incorrect indentation
- Missing closing quotes

---

### E103: Missing Required Frontmatter Field

**Error Message**:
```
Error: Missing required field 'description' in commands/create.md
```

**Cause**: Required frontmatter field is missing

**Component Requirements**:

**Commands**:
- `description` (required)

**Agents**:
- `description` (required)

**Skills**:
- `name` (required)
- `description` (required)

**Example (Wrong)**:
```yaml
---
allowed-tools: ["Read", "Write"]
---
```

**Fix**:
```yaml
---
description: "Creates new items"
allowed-tools: ["Read", "Write"]
---
```

---

### E104: Unclosed Frontmatter

**Error Message**:
```
Error: Frontmatter not properly closed in agents/analyzer.md
Missing closing '---' delimiter
```

**Cause**: Opening `---` without closing `---`

**Example (Wrong)**:
```markdown
---
description: "My agent"

# Agent Content
```

**Fix**:
```markdown
---
description: "My agent"
---

# Agent Content
```

---

## Structure Errors

### E201: Missing Plugin Manifest

**Error Message**:
```
Error: Plugin manifest not found
Expected: .claude-plugin/plugin.json
```

**Cause**: Missing `.claude-plugin/plugin.json` file

**Fix**:
```bash
# Create directory and manifest
mkdir -p .claude-plugin
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My plugin description"
}
EOF
```

---

### E202: No Component Directories

**Error Message**:
```
Warning: No component directories found
Expected at least one of: commands/, agents/, skills/
```

**Cause**: Plugin has no components

**Fix**:
```bash
# Create at least one component directory
mkdir -p commands
# Or
mkdir -p agents
# Or
mkdir -p skills
```

**Rules**:
- Plugin must have at least one of: commands, agents, or skills
- Empty directories are acceptable during development

---

### E203: Missing SKILL.md File

**Error Message**:
```
Error: SKILL.md not found in skills/api-design/
Expected: skills/api-design/SKILL.md
```

**Cause**: Skill directory exists but no SKILL.md file

**Fix**:
```bash
cat > skills/api-design/SKILL.md << 'EOF'
---
name: "api-design"
description: "API design guidance and patterns"
---

# API Design Skill

Skill content here.
EOF
```

**Rules**:
- Every skill directory must have SKILL.md
- File name must be uppercase: `SKILL.md`

---

## Naming Errors

### E301: Skill Name Mismatch

**Error Message**:
```
Error: Skill name 'api-designer' doesn't match directory name 'api-design'
Location: skills/api-design/SKILL.md
Directory: api-design
Frontmatter name: api-designer
```

**Cause**: Skill frontmatter name doesn't match directory name

**Example (Wrong)**:
```
Directory: skills/api-design/

File: skills/api-design/SKILL.md
---
name: "api-designer"  # Doesn't match directory
---
```

**Fix**:
```yaml
---
name: "api-design"  # Matches directory exactly
---
```

**Rules**:
- Skill name in frontmatter must match directory name exactly
- Case-sensitive match required
- Include hyphens if directory has them

---

### E302: Invalid File Name Format

**Error Message**:
```
Warning: File name 'CreateTask.md' should use kebab-case
Expected: create-task.md
```

**Cause**: Component file not using kebab-case

**Examples (Wrong)**:
```
CreateTask.md           # PascalCase
create_task.md          # snake_case
Create-Task.md          # Mixed case
```

**Fix**:
```
create-task.md          # kebab-case
api-analyzer.md         # All lowercase
my-command.md           # Hyphens separate words
```

---

## Tool Errors

### E401: Invalid Tool Name

**Error Message**:
```
Error: Invalid tool 'WriteFile' in commands/generate.md
Valid tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
```

**Cause**: Tool name doesn't match valid Claude Code tools

**Examples (Wrong)**:
```yaml
---
allowed-tools: ["WriteFile", "ReadFile"]     # Wrong names
allowed-tools: ["write", "read"]             # Wrong case
allowed-tools: ["File", "Execute"]           # Not valid tools
---
```

**Fix**:
```yaml
---
allowed-tools: ["Write", "Read"]             # Correct names
allowed-tools: ["Bash", "Grep", "Glob"]      # Valid tools
---
```

**Valid Tools** (case-sensitive):
- `Read` - Read files
- `Write` - Write files
- `Edit` - Edit files
- `Bash` - Execute bash commands
- `Grep` - Search with grep
- `Glob` - Find files by pattern
- `WebFetch` - Fetch web content

---

### E402: Tool Name Case Error

**Error Message**:
```
Error: Invalid tool case 'bash' in commands/deploy.md
Expected: Bash (capitalized)
```

**Cause**: Tool name has incorrect capitalization

**Example (Wrong)**:
```yaml
---
allowed-tools: ["bash", "read", "write"]  # Lowercase
---
```

**Fix**:
```yaml
---
allowed-tools: ["Bash", "Read", "Write"]  # Correct case
---
```

**Rules**:
- All tool names are capitalized: First letter uppercase
- Rest of letters lowercase
- Exception: `WebFetch` (camelCase)

---

## Length Limit Errors

### E501: Description Too Long

**Error Message**:
```
Error: Description exceeds 1024 character limit in agents/analyzer.md
Current length: 1156 characters
Limit: 1024 characters
Exceeds by: 132 characters
```

**Cause**: Agent or skill description exceeds 1024 character limit

**Example (Wrong - 1156 chars)**:
```yaml
---
description: "This agent provides comprehensive analysis of code quality, including but not limited to: syntax checking with multiple linters, style compliance checking against PEP8 and other industry standards, security vulnerability scanning using state-of-the-art tools, performance optimization suggestions based on profiling data, code smell detection across the entire codebase, maintainability metrics calculation and reporting, test coverage analysis with detailed reports, documentation completeness checking against standards, dependency analysis for potential issues, and architectural review with detailed recommendations for improvements across all aspects of the codebase with examples and specific fixes for each identified issue..."
---
```

**Fix (248 chars)**:
```yaml
---
description: "Use this agent for comprehensive code analysis including quality, security, performance, and maintainability checks. Activates for code review, quality assessment, vulnerability scanning, optimization suggestions, and architectural guidance."
---
```

**Tips for Condensing**:
- Remove verbose explanations
- Focus on activation triggers
- Use concise language
- Remove redundant phrases
- Keep key functionality descriptions
- Cut examples from description (put in body)

---

### E502: Argument Hint Too Long

**Error Message**:
```
Warning: Argument hint is very long in commands/create.md
Current: 256 characters
Recommended: Under 100 characters
```

**Cause**: Argument hint is too verbose

**Example (Wrong)**:
```yaml
---
argument-hint: "The name of the plugin to create in kebab-case format followed by optional flags for description, author name, author email, license type, and any other metadata you want to include in the plugin manifest"
---
```

**Fix**:
```yaml
---
argument-hint: "plugin-name [--description DESC] [--author NAME] [--license TYPE]"
---
```

**Rules**:
- Keep under 100 characters
- Show syntax, not explanations
- Use brackets for optional args
- Use uppercase for value placeholders

---

## Syntax Errors

### E601: Unescaped Special Characters

**Error Message**:
```
Error: Unescaped special character in frontmatter
Line 2: description contains unquoted colon
```

**Cause**: Special YAML characters not quoted

**Special Characters in YAML**:
```
: & * # ? | - [ ] { } ! % @ `
```

**Example (Wrong)**:
```yaml
---
description: Command does: X & Y
---
```

**Fix**:
```yaml
---
description: "Command does: X & Y"
---
```

**Rules**:
- Quote strings with special characters
- Use double quotes for consistency
- Escape quotes inside strings: `"He said \"hello\""`

---

### E602: Invalid Array Syntax

**Error Message**:
```
Error: Invalid array syntax in frontmatter
Expected: ["item1", "item2"] or list format
```

**Cause**: Array not properly formatted

**Examples (Wrong)**:
```yaml
---
tools: [Read Write]              # Missing quotes/commas
tools: ["Read", "Write",]        # Trailing comma
tools: [Read, Write]             # Inconsistent quoting
---
```

**Fix (Option 1 - Inline)**:
```yaml
---
tools: ["Read", "Write", "Bash"]
---
```

**Fix (Option 2 - List)**:
```yaml
---
tools:
  - Read
  - Write
  - Bash
---
```

**Rules**:
- Quote all elements
- Separate with commas (inline format)
- No trailing commas
- Or use list format with `-` prefix

---

### E603: Incorrect Indentation

**Error Message**:
```
Error: YAML indentation error
Expected consistent indentation (2 or 4 spaces)
```

**Cause**: Inconsistent or incorrect indentation

**Example (Wrong)**:
```yaml
---
description: "My command"
allowed-tools:
- Read
  - Write      # Inconsistent indent
   - Bash      # Different indent
---
```

**Fix**:
```yaml
---
description: "My command"
allowed-tools:
  - Read
  - Write
  - Bash
---
```

**Rules**:
- Use consistent indentation (2 or 4 spaces)
- Don't mix tabs and spaces
- List items same indent level

---

## Quick Fix Cheat Sheet

### Common JSON Fixes
```bash
# Remove trailing commas
sed -i 's/,\s*}/}/g' plugin.json
sed -i 's/,\s*]/]/g' plugin.json

# Validate JSON
python -m json.tool plugin.json > /dev/null && echo "Valid" || echo "Invalid"
```

### Common YAML Fixes
```bash
# Check frontmatter
for f in commands/*.md agents/*.md; do
  head -1 "$f" | grep -q "^---$" || echo "Missing frontmatter: $f"
done

# Validate YAML (requires PyYAML)
python3 << 'EOF'
import yaml, sys
for f in sys.argv[1:]:
    with open(f) as file:
        content = file.read()
        if content.startswith('---'):
            fm = content.split('---', 2)[1]
            try:
                yaml.safe_load(fm)
                print(f"✓ {f}")
            except yaml.YAMLError as e:
                print(f"✗ {f}: {e}")
EOF
```

### Check Tool Names
```bash
# Find invalid tool names
grep -rn "allowed-tools:" --include="*.md" | \
  grep -v -E "(Read|Write|Edit|Bash|Grep|Glob|WebFetch)"
```

### Check Description Lengths
```bash
# Find descriptions over 1024 chars
for f in agents/*.md skills/*/SKILL.md; do
  desc=$(grep "^description:" "$f" | cut -d'"' -f2)
  len=${#desc}
  [ $len -gt 1024 ] && echo "$f: $len chars (exceeds 1024)"
done
```

---

## Validation Workflow

### Step-by-Step Fix Process

1. **Run Validation**
   ```bash
   /cc-plugins:validate
   ```

2. **Fix Critical Errors First**
   - JSON syntax errors
   - Missing required files
   - Invalid frontmatter

3. **Address Warnings**
   - Description lengths
   - Missing recommendations
   - Style issues

4. **Re-validate**
   ```bash
   /cc-plugins:validate
   ```

5. **Test Plugin**
   - Restart Claude Code
   - Test each command
   - Verify agents activate

---

*Use this reference to quickly identify and fix common plugin validation errors.*
