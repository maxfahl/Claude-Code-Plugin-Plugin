# cc-plugins

**A comprehensive meta-plugin for Claude Code that streamlines plugin development, validation, and maintenance.**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/maxfahl/cc-plugins)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-Production-brightgreen)](https://github.com/maxfahl/cc-plugins)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Commands](#commands)
- [Agents](#agents)
- [Skills](#skills)
- [Plugin Structure](#plugin-structure)
- [Workflows & Use Cases](#workflows--use-cases)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

`cc-plugins` is a Claude Code meta-plugin that helps developers create, validate, debug, and maintain other Claude Code plugins. It ensures compliance with official Anthropic specifications and provides automated tooling for the entire plugin development lifecycle.

This plugin is essential for anyone developing Claude Code plugins, providing:
- **Plugin scaffolding** with correct directory structure and manifest files
- **Specialized agents** for architecture, debugging, and documentation
- **Development skills** for creating and validating plugins
- **Validation** against official Claude Code specifications
- **Debugging utilities** to identify and fix common issues
- **Documentation generation** for your plugins
- **Component templates** for commands, agents, and skills
- **Best practices guidance** through AI assistance

## Features

- **Plugin Scaffolding**: Generate new plugins with correct structure and official specifications
- **Specialized Agents**: Expert AI agents for architecture, debugging, and documentation
- **Development Skills**: Comprehensive guidance for plugin creation and validation
- **Validation Tools**: Validate existing plugins against official Claude Code specifications
- **Debugging Utilities**: Identify and fix common plugin issues with detailed recommendations
- **Documentation Generation**: Auto-generate comprehensive plugin documentation
- **Component Templates**: Pre-built templates for commands, agents, skills, and hooks
- **Specification Compliance**: Ensures all generated code follows official Anthropic guidelines
- **Semantic Versioning**: Automatic version management for plugin releases
- **Comprehensive Testing**: Full test suite for validation and development

## Quick Start

```bash
# Create a new plugin
/cc-plugins:create my-awesome-plugin

# Validate the plugin
/cc-plugins:validate my-awesome-plugin

# Generate documentation
/cc-plugins:document my-awesome-plugin

# Debug plugin issues
/cc-plugins:debug my-awesome-plugin
```

## Installation

### Requirements

- Claude Code (latest version)
- Python 3.8+ (for validation and testing)
- Git (optional, for version control)

### Setup Steps

1. **Clone the plugin to your Claude Code plugins directory:**

```bash
cd ~/.claude/plugins
git clone https://github.com/maxfahl/cc-plugins.git
```

Or manually download and place the plugin folder:

```bash
# Extract the plugin archive
unzip cc-plugins.zip -d ~/.claude/plugins/
```

2. **Install Python dependencies:**

```bash
cd cc-plugins
pip install -r tests/requirements.txt
```

3. **Verify installation:**

```bash
# In Claude Code
/cc-plugins:validate
```

Expected output:
```
✓ Plugin validation PASSED
```

4. **Restart Claude Code to load the plugin**

## Commands

### `/cc-plugins:create`

Creates a new Claude Code plugin with correct structure and official specifications.

**Usage:**
```bash
/cc-plugins:create my-plugin
/cc-plugins:create my-plugin --description "Plugin description"
/cc-plugins:create my-plugin --author "John Doe" --license "Apache-2.0"
```

**What it does:**
1. Validates the plugin name (kebab-case format)
2. Creates the complete directory structure
3. Generates plugin manifest with metadata
4. Creates README.md template
5. Sets up test directory with sample tests
6. Validates the created plugin
7. Provides next steps for development

---

### `/cc-plugins:validate`

Validates a plugin directory against official Claude Code specifications.

**Usage:**
```bash
/cc-plugins:validate
/cc-plugins:validate /path/to/plugin
```

**What it checks:**
- Directory structure and required files
- Manifest format and required fields
- Component YAML frontmatter
- Naming conventions (kebab-case)
- Component discovery

---

### `/cc-plugins:debug`

Debugs and fixes common plugin issues with detailed recommendations.

**Usage:**
```bash
/cc-plugins:debug
/cc-plugins:debug /path/to/plugin
```

**What it analyzes:**
- Directory structure integrity
- Manifest JSON validity
- Component syntax and frontmatter
- Configuration files

---

### `/cc-plugins:document`

Generates comprehensive documentation for a plugin.

**Usage:**
```bash
/cc-plugins:document
/cc-plugins:document /path/to/plugin
```

**What it generates:**
- Complete README.md with all components
- Installation instructions
- Usage examples
- Development guidelines

---

### `/cc-plugins:update`

Updates plugin manifest fields or manages version numbers.

**Usage:**
```bash
# Update manifest fields
/cc-plugins:update description "New description"

# Bump semantic version
/cc-plugins:update --version major
/cc-plugins:update --version minor
/cc-plugins:update --version patch
```

---

## Agents

Specialized AI agents that provide expert assistance for plugin development tasks.

### plugin-architect

**Purpose**: Architectural guidance for Claude Code plugin design and structure.

**Activates when:**
- Designing plugin architecture
- Organizing plugin components
- Reviewing plugin structure
- Getting design pattern guidance
- Planning plugin features
- Understanding Claude Code specifications

**Capabilities:**
- Provides comprehensive architectural guidance
- Reviews plugin structure against best practices
- Recommends design patterns for common scenarios
- Ensures specification compliance
- Advises on component organization
- Suggests improvements and refactoring strategies

**Example:**
```
User: "How should I structure my API documentation plugin?"
Agent: Provides detailed architecture recommendations including
       directory structure, command organization, and component design.
```

---

### plugin-debugger

**Purpose**: Expert diagnosis and resolution of plugin issues and errors.

**Activates when:**
- Plugin has errors or fails validation
- Components don't load properly
- Frontmatter syntax is invalid
- Need troubleshooting help
- Specification violations occur
- Need step-by-step fix instructions

**Capabilities:**
- Diagnoses plugin errors and issues
- Runs validation checks
- Provides root cause analysis
- Delivers step-by-step fix instructions
- Categorizes issues (critical, warnings, info)
- Generates structured debug reports
- Explains common errors with solutions

**Example:**
```
User: "My plugin validation fails with YAML errors"
Agent: Identifies specific YAML syntax issues, provides line-by-line
       fixes with before/after examples, and prevention tips.
```

---

### plugin-documenter

**Purpose**: Professional documentation creation for Claude Code plugins.

**Activates when:**
- Need to write plugin documentation
- Generate README files
- Create usage guides
- Document commands and APIs
- Need installation instructions
- Want comprehensive plugin guides

**Capabilities:**
- Generates comprehensive README.md files
- Documents commands with usage examples
- Documents agents with activation scenarios
- Documents skills with use cases
- Creates API reference documentation
- Ensures documentation completeness
- Follows documentation best practices

**Example:**
```
User: "Generate README for my plugin"
Agent: Reads plugin components, extracts metadata, and generates
       complete README with installation, usage, and examples.
```

---

## Skills

Reusable knowledge and workflows for plugin development.

### plugin-development

**Purpose**: Comprehensive guidance for creating and structuring Claude Code plugins.

**Activates for:**
- Plugin creation and scaffolding
- Building plugin components
- Following Claude Code specifications
- Creating commands, agents, and skills
- Plugin architecture decisions
- Understanding plugin structure

**Provides:**
- Component type explanations (commands, agents, skills, hooks)
- Official specification compliance guidance
- Development workflow (planning → testing)
- Common patterns and examples
- Quick reference for creating components
- Troubleshooting guidance

**Supporting Documentation:**
- `spec-reference.md`: Complete specification reference with validation rules

**Example:**
```
User: "How do I create a new command?"
Skill: Provides command structure, frontmatter requirements, examples,
       and step-by-step creation instructions.
```

---

### plugin-validation

**Purpose**: Expert validation of plugins against official specifications.

**Activates for:**
- Validating plugins
- Checking plugin errors
- Fixing specification violations
- Debugging plugin issues
- Verifying plugin structure
- Checking frontmatter syntax
- Ensuring standards compliance

**Provides:**
- Validation process and scope
- Component-specific validation rules
- Syntax validation (YAML, JSON)
- Error categorization (critical, warnings, info)
- Actionable fix instructions
- Validation tools and scripts

**Supporting Documentation:**
- `common-errors.md`: Comprehensive error catalog with 20+ common errors and fixes

**Example:**
```
User: "Validate my plugin structure"
Skill: Guides through validation process, explains what gets checked,
       provides validation commands, and interprets results.
```

---

## Plugin Structure

### Directory Layout

```
cc-plugins/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/                    # Slash commands
│   ├── create.md               # /cc-plugins:create
│   ├── validate.md             # /cc-plugins:validate
│   ├── debug.md                # /cc-plugins:debug
│   ├── document.md             # /cc-plugins:document
│   └── update.md               # /cc-plugins:update
├── agents/                      # Specialized agents
│   ├── plugin-architect.md     # Architecture guidance
│   ├── plugin-debugger.md      # Error diagnosis
│   └── plugin-documenter.md    # Documentation creation
├── skills/                      # Development skills
│   ├── plugin-development/     # Development guidance
│   │   ├── SKILL.md
│   │   └── spec-reference.md
│   └── plugin-validation/      # Validation guidance
│       ├── SKILL.md
│       └── common-errors.md
├── scripts/                     # Python utilities
│   ├── scaffold-plugin.py
│   ├── validate-plugin.py
│   └── validators.py
├── docs/                        # Documentation
│   ├── development/
│   ├── COMMANDS-REFERENCE.md
│   ├── phase4-completion.md
│   └── phase5-6-completion.md
├── tests/                       # Test suite (179+ tests)
│   ├── test_*.py
│   └── requirements.txt
├── README.md                    # This file
└── .gitignore
```

### Component Types

**Commands** (`commands/`):
- Individual markdown files that define slash commands
- YAML frontmatter specifying description, tools, and model
- Executable bash code following frontmatter

**Agents** (`agents/`):
- Specialized AI assistants for domain-specific tasks
- Trigger-rich descriptions (max 1024 chars)
- Tool declarations for capabilities

**Skills** (`skills/`):
- Reusable knowledge and workflows
- Progressive disclosure with supporting docs
- Activation triggers for relevant contexts

**Scripts** (`scripts/`):
- Python validation and scaffolding utilities
- Used internally by commands

**Tests** (`tests/`):
- Comprehensive pytest test suite
- 179+ tests covering all functionality

---

## Workflows & Use Cases

### Workflow 1: Creating Your First Plugin

1. **Create the plugin structure:**
   ```bash
   /cc-plugins:create my-first-plugin
   ```

2. **Navigate to the plugin directory:**
   ```bash
   cd my-first-plugin
   ```

3. **Create your first command:**
   - Create `commands/hello.md` with command definition
   - Include YAML frontmatter with description and tools

4. **Validate your plugin:**
   ```bash
   /cc-plugins:validate
   ```

5. **Generate documentation:**
   ```bash
   /cc-plugins:document
   ```

6. **Test your plugin:**
   ```bash
   pytest tests/ -v
   ```

### Workflow 2: Getting Architectural Advice

1. **Ask for architecture guidance:**
   ```
   "How should I structure my code analysis plugin?"
   ```

2. **plugin-architect agent activates** and provides:
   - Recommended directory structure
   - Component organization advice
   - Design patterns for your use case
   - Best practices guidance

3. **Implement the recommended structure**

4. **Validate against specifications:**
   ```bash
   /cc-plugins:validate
   ```

### Workflow 3: Debugging Plugin Issues

1. **Run validation and see errors:**
   ```bash
   /cc-plugins:validate
   ```

2. **Get detailed debugging help:**
   ```bash
   /cc-plugins:debug
   ```

3. **plugin-debugger agent provides:**
   - Root cause analysis
   - Step-by-step fix instructions
   - Before/after code examples
   - Prevention tips

4. **Apply fixes and re-validate:**
   ```bash
   /cc-plugins:validate
   ```

### Workflow 4: Publishing a Plugin

1. **Ensure plugin is valid:**
   ```bash
   /cc-plugins:validate
   ```

2. **Generate documentation:**
   ```bash
   /cc-plugins:document
   ```

3. **Bump version:**
   ```bash
   /cc-plugins:update --version minor
   ```

4. **Run full test suite:**
   ```bash
   pytest tests/ --cov -v
   ```

5. **Commit and publish:**
   ```bash
   git add .
   git commit -m "Release v1.1.0"
   git tag v1.1.0
   git push origin main --tags
   ```

---

## Troubleshooting

### Issue: "Plugin name must be in kebab-case"

**Solution:**
Use lowercase letters, numbers, and hyphens only.

```bash
# Correct:
/cc-plugins:create my-plugin
/cc-plugins:create my-awesome-plugin
```

### Issue: "Missing required field: version"

**Solution:**
Add version field to `.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description"
}
```

### Issue: "Command missing frontmatter"

**Solution:**
Add YAML frontmatter to command markdown:

```yaml
---
description: "Brief description of what this command does"
allowed-tools: ["Bash", "Read", "Write"]
---

# Your command content here
```

### Getting More Help

1. **Run debug command:**
   ```bash
   /cc-plugins:debug my-plugin
   ```

2. **Ask the plugin-debugger agent:**
   ```
   "My plugin has validation errors, help me fix them"
   ```

3. **Consult plugin-validation skill:**
   ```
   "How do I validate my plugin?"
   ```

---

## Documentation

### Plugin Documentation

- **[Commands Reference](docs/COMMANDS-REFERENCE.md)**: Detailed command documentation
- **[Phase 4 Completion](docs/phase4-completion.md)**: Commands implementation details
- **[Phase 5-6 Completion](docs/phase5-6-completion.md)**: Agents and skills details

### Official References

- [Claude Code Documentation](https://code.claude.com/docs)
- [Plugin Development Guide](https://code.claude.com/docs/en/plugin-development)
- [Component Authoring](https://code.claude.com/docs/en/components)

---

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agents.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

- 179+ tests covering all functionality
- Commands: 32 tests
- Agents: 24 tests
- Skills: 18 tests
- Validation: 105+ tests

### Contributing

Contributions welcome! Please ensure:

1. **All tests pass:**
   ```bash
   pytest tests/ -v
   ```

2. **New features include tests**

3. **Code follows specifications:**
   - Use official plugin manifest format
   - Follow component authoring guidelines
   - Maintain kebab-case naming

4. **Documentation updated:**
   ```bash
   /cc-plugins:document
   ```

5. **Validation passes:**
   ```bash
   /cc-plugins:validate
   ```

---

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:

- **GitHub Issues**: [Report Issues](https://github.com/maxfahl/cc-plugins/issues)
- **GitHub Discussions**: [Ask Questions](https://github.com/maxfahl/cc-plugins/discussions)
- **Documentation**: [View Docs](docs/)
- **Official Claude Code Docs**: [code.claude.com](https://code.claude.com/docs)

---

**Created with ❤️ for the Claude Code community**

Built by Max Fahl | [GitHub](https://github.com/maxfahl) | [Website](https://maxfahl.com)
