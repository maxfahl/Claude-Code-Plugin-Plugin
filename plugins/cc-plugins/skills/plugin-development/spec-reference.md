# Claude Code Plugin Specification Reference

Quick reference guide for official Claude Code plugin specifications.

## Plugin Structure

### Required
```
plugin-name/
└── .claude-plugin/
    └── plugin.json         # Plugin manifest (REQUIRED)
```

### Standard Structure
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json         # Manifest
├── commands/               # Slash commands
│   └── *.md
├── agents/                 # Specialized agents
│   └── *.md
├── skills/                 # Reusable skills
│   └── skill-name/
│       └── SKILL.md
├── hooks/                  # Event hooks (optional)
├── scripts/                # Utility scripts (optional)
├── tests/                  # Test suite (recommended)
├── docs/                   # Documentation (optional)
└── README.md               # Documentation (recommended)
```

## Manifest Schema (plugin.json)

### Required Fields
```json
{
  "name": "plugin-name",        // kebab-case, unique
  "version": "1.0.0",           // semantic versioning
  "description": "Plugin desc"  // brief description
}
```

### Complete Schema
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description of plugin",
  "author": {
    "name": "Author Name",
    "email": "email@example.com",
    "url": "https://example.com"
  },
  "license": "MIT",
  "homepage": "https://github.com/user/plugin-name",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/plugin-name.git"
  },
  "keywords": ["keyword1", "keyword2"],
  "dependencies": {}
}
```

### Validation Rules
- Must be valid JSON (no trailing commas)
- `name` must be kebab-case
- `version` must follow semantic versioning (MAJOR.MINOR.PATCH)
- All strings must be quoted

## Command Specification

### File Location
```
commands/command-name.md
```

### Frontmatter Schema
```yaml
---
description: "What command does"                    # Required
allowed-tools: ["Bash", "Read", "Write"]           # Optional
argument-hint: "Expected arguments"                # Optional
model: "sonnet"                                    # Optional: sonnet|opus|haiku
---
```

### Command Structure
```markdown
---
description: "Command description"
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "argument-name [optional-arg]"
model: "sonnet"
---

# Command Name

Documentation for the command.

## Usage

Examples and instructions.

---

!bash
# Actual command implementation
echo "Command logic here"
```

### Requirements
- Must have valid YAML frontmatter
- `description` field required
- Frontmatter must be closed with `---`
- Bash script follows final `---` and `!bash` marker

## Agent Specification

### File Location
```
agents/agent-name.md
```

### Frontmatter Schema
```yaml
---
description: "What agent does and when to use (max 1024 chars)"  # Required
tools: ["Read", "Write", "Grep"]                                 # Optional
model: "sonnet"                                                  # Optional
---
```

### Agent Structure
```markdown
---
description: "Detailed description with activation triggers (max 1024 chars)"
tools: ["Read", "Write", "Grep"]
model: "sonnet"
---

# Agent Name

Agent instructions and expertise.

## Purpose
What this agent specializes in.

## When to Use
Activation scenarios.

## Examples
Usage examples.
```

### Requirements
- Must have valid YAML frontmatter
- `description` field required, max 1024 characters
- Description should include activation triggers
- Frontmatter must be closed with `---`

## Skill Specification

### Directory Structure
```
skills/
└── skill-name/              # Directory name = skill identifier
    ├── SKILL.md             # Required: Main skill file
    ├── reference.md         # Optional: Supporting docs
    └── examples.md          # Optional: More docs
```

### Frontmatter Schema
```yaml
---
name: "skill-name"                    # Required, must match directory
description: "Skill description"      # Required, max 1024 chars
allowed-tools: ["Read", "Write"]      # Optional
version: "1.0.0"                      # Optional
---
```

### Skill Structure
```markdown
---
name: "skill-name"
description: "When to activate and what skill provides (max 1024 chars)"
allowed-tools: ["Read", "Write"]
version: "1.0.0"
---

# Skill Name

Skill knowledge and instructions.

## Overview
What this skill provides.

## When to Activate
Activation scenarios.

## Usage
How to use this skill.
```

### Requirements
- Directory name must match `name` field exactly
- Must have valid YAML frontmatter
- `name` and `description` fields required
- Description max 1024 characters
- SKILL.md must exist in skill directory

## Hook Specification

### File Location
```
hooks/event-name.md
```

### Common Hook Types
- `on-save.md` - Triggered when files are saved
- `on-open.md` - Triggered when files are opened
- `on-close.md` - Triggered when files are closed

### Hook Structure
```markdown
---
description: "What hook does"
event: "save"                        # Event type
pattern: "**/*.py"                   # File pattern (optional)
---

# Hook Name

Hook logic and instructions.
```

## Naming Conventions

### Plugin Names
- **Format**: kebab-case
- **Examples**: `my-plugin`, `api-helper`, `code-validator`
- **Invalid**: `MyPlugin`, `my_plugin`, `My Plugin`

### File Names
- **Format**: kebab-case with `.md` extension
- **Examples**: `create-task.md`, `api-analyzer.md`
- **Invalid**: `CreateTask.md`, `create_task.md`

### Skill Directory Names
- **Format**: kebab-case
- **Must match**: Skill frontmatter `name` field exactly
- **Examples**: `api-design`, `error-handling`

## Tool Names (Case-Sensitive)

Valid tool names for `allowed-tools` and `tools` fields:

- `Read` - Read files from filesystem
- `Write` - Write files to filesystem
- `Edit` - Edit existing files
- `Bash` - Execute bash commands
- `Grep` - Search with grep/ripgrep
- `Glob` - Find files by pattern
- `WebFetch` - Fetch content from web

**Note**: Tool names are case-sensitive. Use exact capitalization.

## Frontmatter Format

### YAML Requirements
- Must start with `---`
- Must end with `---`
- Must be valid YAML syntax
- Keys and values must be properly formatted

### String Values
```yaml
# Simple strings (no special characters)
description: My description

# Strings with special characters (use quotes)
description: "My description: with colon"

# Long strings (use quotes)
description: "This is a longer description that spans multiple words"
```

### Array Values
```yaml
# List format
tools:
  - Read
  - Write
  - Bash

# Inline format (preferred for short lists)
tools: ["Read", "Write", "Bash"]
```

### Boolean Values
```yaml
enabled: true
disabled: false
```

## Character Limits

| Component | Field | Limit |
|-----------|-------|-------|
| Agent | description | 1024 chars |
| Skill | description | 1024 chars |
| Command | description | No hard limit |
| Manifest | description | No hard limit |

**Best Practice**: Keep all descriptions concise and focused.

## Version Format

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Examples**: `1.0.0`, `2.3.1`, `0.1.0`

## Directory Permissions

Ensure proper permissions:
```bash
chmod 755 .claude-plugin commands agents skills hooks scripts
chmod 644 .claude-plugin/plugin.json
chmod 644 commands/*.md agents/*.md skills/*/SKILL.md
```

## Validation Checklist

### Manifest Validation
- [ ] File exists at `.claude-plugin/plugin.json`
- [ ] Valid JSON syntax
- [ ] Required fields present: name, version, description
- [ ] Plugin name is kebab-case
- [ ] Version follows semantic versioning

### Command Validation
- [ ] Files in `commands/` directory
- [ ] `.md` file extension
- [ ] Valid YAML frontmatter
- [ ] Description field present
- [ ] Frontmatter properly closed with `---`
- [ ] Tool names are valid and case-correct

### Agent Validation
- [ ] Files in `agents/` directory
- [ ] `.md` file extension
- [ ] Valid YAML frontmatter
- [ ] Description field present and under 1024 chars
- [ ] Description includes activation triggers
- [ ] Frontmatter properly closed with `---`

### Skill Validation
- [ ] Directory in `skills/` folder
- [ ] `SKILL.md` file exists in skill directory
- [ ] Valid YAML frontmatter
- [ ] Name field matches directory name exactly
- [ ] Description field present and under 1024 chars
- [ ] Frontmatter properly closed with `---`

## Common Errors

### Invalid JSON
```json
// WRONG - trailing comma
{
  "name": "my-plugin",
  "version": "1.0.0",
}

// CORRECT
{
  "name": "my-plugin",
  "version": "1.0.0"
}
```

### Invalid YAML
```yaml
# WRONG - unquoted special characters
---
description: Command does: X & Y
---

# CORRECT
---
description: "Command does: X & Y"
---
```

### Wrong Tool Name
```yaml
# WRONG - incorrect case or name
---
allowed-tools: ["read", "write", "bash"]
---

# CORRECT
---
allowed-tools: ["Read", "Write", "Bash"]
---
```

### Skill Name Mismatch
```
# Directory: skills/api-design/

# WRONG - name doesn't match directory
---
name: "api-designer"
---

# CORRECT
---
name: "api-design"
---
```

## Official Resources

- **Claude Code Documentation**: https://docs.anthropic.com/
- **Plugin Development Guide**: Official Anthropic documentation
- **Example Plugins**: Reference implementations from Anthropic

## Quick Validation Commands

```bash
# Validate JSON
python -m json.tool .claude-plugin/plugin.json

# Check YAML frontmatter
grep -A 10 "^---" commands/*.md

# Find missing descriptions
grep -L "description:" agents/*.md

# Check kebab-case naming
ls -1 | grep -v "^[a-z0-9-]*$"
```

---

*This reference summarizes official Claude Code plugin specifications. Always refer to official Anthropic documentation for authoritative guidance.*
