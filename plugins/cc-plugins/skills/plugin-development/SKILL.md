---
name: "plugin-development"
description: "Expert guidance for creating, structuring, and developing Claude Code plugins. Activate for plugin creation, plugin scaffolding, building plugin components, following Claude Code specifications, creating commands/agents/skills, plugin architecture decisions, or understanding plugin structure. Ensures compliance with official Anthropic specifications."
allowed-tools: ["Read", "Write", "Bash", "Grep", "Glob"]
version: "1.0.0"
---

# Plugin Development Skill

Comprehensive guidance for developing Claude Code plugins from scratch, following official Anthropic specifications.

## Overview

This skill provides expert knowledge for:
- Creating new Claude Code plugins
- Structuring plugin components correctly
- Writing commands, agents, and skills
- Following official specifications
- Implementing best practices
- Ensuring specification compliance

## When to Activate

This skill activates when you need to:
- Create a new Claude Code plugin
- Add components to an existing plugin
- Understand plugin structure requirements
- Follow official Anthropic specifications
- Make architectural decisions for plugins
- Learn plugin development best practices
- Implement commands, agents, or skills
- Structure plugin directories correctly

## Core Concepts

### What is a Claude Code Plugin?

A Claude Code plugin extends Claude Code functionality through:
- **Commands**: Slash commands users invoke directly (e.g., `/plugin:create`)
- **Agents**: Specialized AI assistants for domain-specific tasks
- **Skills**: Reusable knowledge and workflows
- **Hooks**: Event-driven automation (optional)

### Plugin Structure

Official structure for Claude Code plugins:

```
plugin-name/                    # Plugin root (kebab-case)
├── .claude-plugin/
│   └── plugin.json            # Required: Plugin manifest
├── commands/                   # Optional: Slash commands
│   ├── command1.md
│   └── command2.md
├── agents/                     # Optional: Specialized agents
│   ├── agent1.md
│   └── agent2.md
├── skills/                     # Optional: Reusable skills
│   ├── skill1/
│   │   ├── SKILL.md           # Required skill file
│   │   └── supporting-docs.md
│   └── skill2/
│       └── SKILL.md
├── hooks/                      # Optional: Event hooks
│   └── on-save.md
├── scripts/                    # Optional: Utility scripts
│   └── validate.py
├── docs/                       # Optional: Documentation
│   └── guide.md
├── tests/                      # Recommended: Test suite
│   └── test_plugin.py
├── README.md                   # Recommended: Plugin documentation
└── .gitignore                  # Recommended: Git ignore file
```

### Required vs Optional

**Required**:
- `.claude-plugin/plugin.json` - Plugin manifest
- At least one of: commands/, agents/, or skills/

**Recommended**:
- `README.md` - Documentation
- `tests/` - Test suite
- `.gitignore` - Git ignore rules

**Optional**:
- `hooks/` - Event-driven automation
- `scripts/` - Utility scripts
- `docs/` - Additional documentation

## Component Types

### 1. Commands (`commands/*.md`)

Slash commands that users invoke directly.

**When to use**: User needs explicit, direct action with specific arguments.

**Structure**:
```markdown
---
description: "What command does and when to use it"
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "Expected arguments description"
model: "sonnet"  # optional: sonnet, opus, haiku
---

# Command Name

Command documentation here.

## Usage

Examples and documentation.

---

!bash
# Actual bash script that executes
echo "Command logic here"
```

**Frontmatter Requirements**:
- `description`: Required. What command does.
- `allowed-tools`: Optional but recommended. Array of tool names.
- `argument-hint`: Optional. Hint about expected arguments.
- `model`: Optional. AI model to use (sonnet, opus, haiku).

**Best Practices**:
- Single responsibility per command
- Clear, descriptive names
- Validate inputs
- Provide helpful error messages
- Include usage examples

### 2. Agents (`agents/*.md`)

Specialized AI assistants for domain-specific tasks.

**When to use**: Complex analysis, generation, or domain expertise needed.

**Structure**:
```markdown
---
description: "When to use agent and what it does (max 1024 chars)"
tools: ["Read", "Write", "Grep"]  # optional
model: "sonnet"  # optional: sonnet, opus, haiku
---

# Agent Name

Agent instructions and expertise description.

## Purpose

What this agent specializes in.

## When to Use

Activation scenarios.

## Examples

Usage examples showing agent in action.
```

**Frontmatter Requirements**:
- `description`: Required. Max 1024 characters. Include activation triggers.
- `tools`: Optional. Array of tool names agent can use.
- `model`: Optional. AI model preference.

**Best Practices**:
- Focused specialization (one domain)
- Trigger-rich descriptions
- Clear activation scenarios
- Comprehensive instructions
- Example use cases

### 3. Skills (`skills/*/SKILL.md`)

Reusable knowledge and workflows.

**When to use**: Knowledge that multiple agents/commands can leverage.

**Structure**:
```
skills/
└── skill-name/           # Directory name = skill identifier
    ├── SKILL.md          # Required: Main skill file
    ├── reference.md      # Optional: Supporting docs
    └── examples.md       # Optional: Examples
```

**SKILL.md Format**:
```markdown
---
name: "skill-name"  # Must match directory name
description: "When to activate and what skill provides (max 1024 chars)"
allowed-tools: ["Read", "Write"]  # optional
version: "1.0.0"  # optional but recommended
---

# Skill Name

Skill knowledge and instructions.

## Overview

What this skill provides.

## When to Activate

Trigger scenarios.

## Usage

How to use this skill.
```

**Frontmatter Requirements**:
- `name`: Required. Must match directory name exactly.
- `description`: Required. Max 1024 characters. Include triggers.
- `allowed-tools`: Optional. Tools skill can use.
- `version`: Optional but recommended.

**Best Practices**:
- Progressive disclosure (reference supporting docs)
- Clear activation triggers
- Reusable across contexts
- Well-organized supporting documentation
- Version controlled

## Plugin Manifest (plugin.json)

Required file at `.claude-plugin/plugin.json`.

**Minimum Structure**:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief plugin description"
}
```

**Complete Structure**:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Comprehensive description of what plugin does",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "license": "MIT",
  "homepage": "https://github.com/user/plugin-name",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/plugin-name.git"
  },
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "dependencies": {}
}
```

**Field Requirements**:
- `name`: Required. Kebab-case string. Must be unique.
- `version`: Required. Semantic versioning (e.g., "1.0.0").
- `description`: Required. Brief description of plugin.
- `author`: Optional but recommended. Author information.
- `license`: Optional but recommended. License identifier.
- `keywords`: Optional. Array of relevant keywords.

**Validation Rules**:
- Must be valid JSON (no trailing commas)
- Name must be kebab-case (lowercase with hyphens)
- Version must follow semantic versioning
- All string values must be quoted

## Development Workflow

### 1. Planning Phase

Before coding, define:
- **Purpose**: What problem does plugin solve?
- **Components**: What commands/agents/skills needed?
- **Structure**: How to organize functionality?
- **Dependencies**: What tools/libraries required?

### 2. Scaffolding Phase

Create plugin structure:
```bash
# Using cc-plugins meta-plugin
/cc-plugins:create my-plugin --description "My plugin description"

# Or manually
mkdir -p my-plugin/{.claude-plugin,commands,agents,skills,tests,docs}
```

Create manifest:
```bash
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description"
}
EOF
```

### 3. Implementation Phase

Build components incrementally:

**Step 1**: Create basic command
```bash
cat > my-plugin/commands/hello.md << 'EOF'
---
description: "Says hello"
allowed-tools: ["Bash"]
---

# Hello Command

!bash
echo "Hello from my-plugin!"
EOF
```

**Step 2**: Test command works
```bash
# Restart Claude Code
# Try: /my-plugin:hello
```

**Step 3**: Add more components as needed

### 4. Validation Phase

Validate plugin structure:
```bash
# If using cc-plugins
/cc-plugins:validate my-plugin

# Or manual checks
- Check manifest JSON is valid
- Check frontmatter in all components
- Check naming conventions
- Check required fields present
```

### 5. Documentation Phase

Document your plugin:
```bash
# Generate README
/cc-plugins:document my-plugin

# Or write manually following documentation standards
```

### 6. Testing Phase

Write and run tests:
```python
# tests/test_plugin.py
import pytest

def test_plugin_structure():
    """Test that plugin structure is valid."""
    assert Path(".claude-plugin/plugin.json").exists()

def test_manifest_valid():
    """Test that manifest is valid JSON."""
    with open(".claude-plugin/plugin.json") as f:
        manifest = json.load(f)
    assert "name" in manifest
    assert "version" in manifest
```

## Official Specifications

### Naming Conventions

- **Plugin names**: kebab-case (e.g., `my-awesome-plugin`)
- **File names**: kebab-case (e.g., `create-task.md`)
- **Directory names**: kebab-case (e.g., `task-management/`)
- **Skill names**: Must match directory name exactly

### Frontmatter Format

Always YAML format between `---` delimiters:
```yaml
---
key: "value"
list: ["item1", "item2"]
---
```

Rules:
- Must start file with `---`
- Must close with `---`
- Must be valid YAML
- Quote strings with special characters
- Use arrays for lists

### Tool Names

Valid tool names (case-sensitive):
- `Read` - Read files
- `Write` - Write files
- `Edit` - Edit files
- `Bash` - Execute bash commands
- `Grep` - Search with grep
- `Glob` - Find files by pattern
- `WebFetch` - Fetch web content

### Description Length Limits

- **Commands**: No hard limit, but keep concise
- **Agents**: Max 1024 characters
- **Skills**: Max 1024 characters

Focus on activation triggers and core functionality.

## Common Patterns

### Pattern 1: Command + Agent

**Use case**: Command for user invocation, agent for AI assistance

```
commands/
  └── analyze.md       # User runs /plugin:analyze file.txt

agents/
  └── analyzer.md      # Agent provides analysis expertise
```

### Pattern 2: Skill-Based Plugin

**Use case**: Reusable knowledge across contexts

```
skills/
  ├── api-design/
  │   ├── SKILL.md
  │   └── rest-patterns.md
  └── error-handling/
      └── SKILL.md
```

### Pattern 3: Command Suite

**Use case**: Multiple related commands

```
commands/
  ├── create.md        # Create new item
  ├── update.md        # Update existing item
  ├── delete.md        # Delete item
  └── list.md          # List all items
```

### Pattern 4: Workflow Automation

**Use case**: Multi-step workflow commands

```
commands/
  └── deploy.md        # Orchestrates: build → test → deploy

agents/
  └── deployer.md      # Handles deployment logic
```

## Troubleshooting

### Plugin Doesn't Load

**Check**:
- Plugin is in `~/.claude/plugins/` directory
- `.claude-plugin/plugin.json` exists and is valid JSON
- Plugin name in manifest matches directory name
- Restarted Claude Code after adding plugin

### Command Doesn't Appear

**Check**:
- Command file is in `commands/` directory
- File has `.md` extension
- Frontmatter is valid YAML
- Description field is present
- File is not empty

### Agent Doesn't Activate

**Check**:
- Agent file is in `agents/` directory
- Description includes activation triggers
- Description is under 1024 characters
- Frontmatter is properly closed with `---`

### Skill Not Found

**Check**:
- Skill directory name matches frontmatter `name` field exactly
- SKILL.md file exists in skill directory
- Frontmatter is valid YAML
- Description includes activation triggers

## Resources

### Reference Documentation

See supporting documentation:
- `spec-reference.md` - Official specification summary
- Claude Code documentation - https://docs.anthropic.com/

### Example Plugins

Study existing plugins for patterns:
- cc-plugins - Meta-plugin for plugin development
- Official Anthropic examples

### Tools

Helpful tools:
- `/cc-plugins:create` - Scaffold new plugins
- `/cc-plugins:validate` - Validate plugin structure
- `/cc-plugins:debug` - Debug plugin issues
- `/cc-plugins:document` - Generate documentation

## Quick Reference

### Create New Plugin
```bash
/cc-plugins:create my-plugin
```

### Add Command
```bash
cat > commands/my-command.md << 'EOF'
---
description: "Command description"
allowed-tools: ["Bash"]
---

# My Command

!bash
echo "Command logic"
EOF
```

### Add Agent
```bash
cat > agents/my-agent.md << 'EOF'
---
description: "Agent description with triggers"
tools: ["Read", "Write"]
---

# My Agent

Agent instructions here.
EOF
```

### Add Skill
```bash
mkdir -p skills/my-skill
cat > skills/my-skill/SKILL.md << 'EOF'
---
name: "my-skill"
description: "Skill description"
---

# My Skill

Skill knowledge here.
EOF
```

### Validate Plugin
```bash
/cc-plugins:validate
```

---

*Use this skill when developing Claude Code plugins to ensure compliance with official specifications and best practices.*
