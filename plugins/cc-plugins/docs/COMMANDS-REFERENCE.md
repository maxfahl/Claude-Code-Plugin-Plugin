# cc-plugins Commands Reference

Quick reference guide for all `/cc-plugins` commands.

## Commands Overview

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `/cc-plugins:create` | Create new plugins | Scaffolds full structure, generates manifest |
| `/cc-plugins:validate` | Validate plugins | Checks specs, manifest, frontmatter |
| `/cc-plugins:update` | Update plugin info | Manifest fields, semantic versioning |
| `/cc-plugins:document` | Generate docs | Auto-creates comprehensive README |
| `/cc-plugins:debug` | Debug issues | Checks structure, suggests fixes |

---

## 1. Create Plugin

**Command**: `/cc-plugins:create`

**Description**: Create a new Claude Code plugin with correct structure and specifications.

**Usage**:
```bash
/cc-plugins:create <plugin-name> [options]
```

**Options**:
- `--description`: Plugin description
- `--author`: Author name
- `--license`: License type (default: MIT)

**Examples**:
```bash
# Basic plugin
/cc-plugins:create my-plugin

# With metadata
/cc-plugins:create my-plugin \
  --description "A helpful plugin" \
  --author "Jane Developer" \
  --license "Apache-2.0"
```

**Creates**:
- `.claude-plugin/plugin.json` - Manifest
- `commands/` - Commands directory
- `agents/` - Agents directory
- `skills/` - Skills directory
- `scripts/` - Scripts directory
- `docs/` - Documentation
- `tests/` - Test suite
- `README.md` - Initial documentation
- `.gitignore` - Git configuration

---

## 2. Validate Plugin

**Command**: `/cc-plugins:validate`

**Description**: Validate a plugin against official Claude Code specifications.

**Usage**:
```bash
/cc-plugins:validate [path]
```

**Arguments**:
- `path`: Optional. Directory to validate (default: current directory)

**Examples**:
```bash
# Validate current directory
/cc-plugins:validate

# Validate specific plugin
/cc-plugins:validate ./my-plugin

# Validate absolute path
/cc-plugins:validate /path/to/plugin
```

**Checks**:
- Directory structure compliance
- Manifest format and validity
- Required fields (name, version)
- Kebab-case naming
- Component files and frontmatter

**Output**: Summary of passed checks and any errors/warnings

---

## 3. Update Plugin

**Command**: `/cc-plugins:update`

**Description**: Update plugin manifest fields or bump version numbers.

**Usage**:
```bash
/cc-plugins:update <field> <value>
/cc-plugins:update --version <major|minor|patch>
```

**Examples**:
```bash
# Update description
/cc-plugins:update description "New description"

# Update version directly
/cc-plugins:update version 2.0.0

# Bump semantic version
/cc-plugins:update --version major    # 1.0.0 → 2.0.0
/cc-plugins:update --version minor    # 1.0.0 → 1.1.0
/cc-plugins:update --version patch    # 1.0.0 → 1.0.1

# Update nested fields
/cc-plugins:update author.name "John Developer"
/cc-plugins:update author.email "john@example.com"

# Add keywords
/cc-plugins:update keywords "useful"
```

**Features**:
- Backs up manifest before changes
- Validates after updates
- Restores on validation failure
- Shows confirmation before applying

---

## 4. Document Plugin

**Command**: `/cc-plugins:document`

**Description**: Generate comprehensive documentation from plugin files.

**Usage**:
```bash
/cc-plugins:document [path]
```

**Arguments**:
- `path`: Optional. Plugin directory (default: current directory)

**Examples**:
```bash
# Document current directory
/cc-plugins:document

# Document specific plugin
/cc-plugins:document ./my-plugin
```

**Generates**:
- `README.md` with complete documentation
- Plugin metadata section (name, version, author)
- Installation instructions
- Features overview
- Quick start guide
- All commands documentation
- All agents documentation
- All skills documentation
- Development section
- Testing instructions
- Contributing guidelines
- License information

---

## 5. Debug Plugin

**Command**: `/cc-plugins:debug`

**Description**: Debug and identify plugin issues with fix suggestions.

**Usage**:
```bash
/cc-plugins:debug [path]
```

**Arguments**:
- `path`: Optional. Plugin directory (default: current directory)

**Examples**:
```bash
# Debug current directory
/cc-plugins:debug

# Debug specific plugin
/cc-plugins:debug ./my-plugin
```

**Checks**:
- Directory structure integrity
- Manifest JSON validity
- Required manifest fields
- Kebab-case naming
- Component file frontmatter
- Required frontmatter fields
- File syntax errors
- Script executeability

**Reports**:
- Critical issues (must fix)
- Warnings (recommended)
- Specific fix suggestions
- Code examples for fixes
- Next steps

---

## Workflow Examples

### Create and Validate a New Plugin

```bash
# 1. Create plugin
/cc-plugins:create my-awesome-plugin \
  --description "My awesome plugin" \
  --author "Me"

# 2. Change to plugin directory
cd my-awesome-plugin

# 3. Validate structure
/cc-plugins:validate

# 4. Debug any issues
/cc-plugins:debug

# 5. Generate documentation
/cc-plugins:document
```

### Update Plugin Version and Release

```bash
cd my-plugin

# Update version
/cc-plugins:update --version minor

# Update description for release
/cc-plugins:update description "Release version 1.1.0 with new features"

# Validate before release
/cc-plugins:validate

# Regenerate documentation
/cc-plugins:document

# Check everything is good
/cc-plugins:debug
```

### Maintain Existing Plugin

```bash
cd existing-plugin

# Regular validation
/cc-plugins:validate

# Find and fix issues
/cc-plugins:debug

# Update documentation
/cc-plugins:document

# Update metadata if needed
/cc-plugins:update author.email "new@example.com"
```

---

## Exit Codes

All commands return:
- **0**: Success
- **1**: Error/Failure

---

## Common Issues & Solutions

### Issue: Plugin name must be in kebab-case

**Solution**:
```bash
# Fix in .claude-plugin/plugin.json
# Change from: "name": "MyPlugin"
# Change to: "name": "my-plugin"
```

### Issue: Missing required manifest fields

**Solution**:
```bash
# Add missing fields to .claude-plugin/plugin.json
# Required: name, version
# Recommended: description, author, license
```

### Issue: Command missing frontmatter

**Solution**:
```bash
# Add frontmatter to top of command file (e.g., commands/my-cmd.md)
---
description: "What this command does"
allowed-tools: ["Bash", "Read", "Write"]
---
```

### Issue: Validation fails

**Solution**:
```bash
# Run debug command for detailed analysis
/cc-plugins:debug

# Fix issues identified
# Re-validate
/cc-plugins:validate
```

---

## Tips & Tricks

### 1. Always validate before publishing
```bash
/cc-plugins:validate
```

### 2. Keep documentation up to date
```bash
# Regenerate docs after changes
/cc-plugins:document
```

### 3. Use semantic versioning
```bash
# Major: breaking changes
/cc-plugins:update --version major

# Minor: new features, backward compatible
/cc-plugins:update --version minor

# Patch: bug fixes
/cc-plugins:update --version patch
```

### 4. Debug before asking for help
```bash
/cc-plugins:debug
# Follow suggestions to fix issues
```

### 5. Keep backups safe
- The `update` command automatically backs up manifest
- Backups named `plugin.json.backup`
- Check for backups if something goes wrong

---

## Model Selection

All commands default to `sonnet` model for optimal performance:
- Fast execution
- Good for CLI output formatting
- Efficient parsing and validation

---

## Need Help?

For each command:
- Use `-h` or `--help` for usage info (when available)
- Run `/cc-plugins:debug` to identify issues
- Check command documentation with `/cc-plugins:document`
- Review official specifications in plugin documentation

---

## Command Files Location

```
~/.claude/plugins/cc-plugins/commands/
├── create.md
├── validate.md
├── update.md
├── document.md
└── debug.md
```

All commands are available immediately after plugin installation.
