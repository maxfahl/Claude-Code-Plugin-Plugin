# Helper Scripts Reference Guide

## Quick Reference

Three utility scripts for plugin validation and analysis:

| Script | Purpose | Key Feature |
|--------|---------|-------------|
| `check-formats.py` | Format validation | YAML/JSON/markdown syntax checking |
| `inspect-components.py` | Component analysis | Lists all components with metadata |
| `check-spec-compliance.py` | Spec validation | Detects non-compliance and deprecations |

## Installation & Setup

All scripts are executable and located in `scripts/`:

```bash
cd /path/to/cc-plugins

# Make scripts executable (already done)
chmod +x scripts/check-formats.py
chmod +x scripts/inspect-components.py
chmod +x scripts/check-spec-compliance.py

# Verify dependencies
pip install pyyaml  # Required for all scripts
```

## Script 1: check-formats.py

### Purpose
Validates file format syntax across your plugin.

### Syntax
```bash
./scripts/check-formats.py [OPTIONS] [PATH]
```

### Options
- `PATH`: Plugin directory (default: current directory)
- `--json-only`: Check only JSON files
- `--md-only`: Check only markdown files
- `--json-output`: Output results as JSON
- `--help`: Show help message

### What It Checks

**Markdown Files**:
- YAML frontmatter syntax (commands, agents, skills)
- Matching opening/closing `---` delimiters
- Trailing whitespace
- Missing final newline

**JSON Files**:
- `plugin.json`: Plugin manifest syntax
- `hooks.json`: Git hooks configuration
- `.mcp.json`: MCP server configuration

### Examples

```bash
# Check everything
./scripts/check-formats.py

# Check specific plugin
./scripts/check-formats.py /path/to/plugin

# Check only JSON
./scripts/check-formats.py --json-only .

# JSON output for CI/CD
./scripts/check-formats.py --json-output . | jq .
```

### Exit Codes
- `0`: All formats valid
- `1`: Format errors found
- `2`: Script execution error

### Output Format

**Text (default)**:
```
FORMAT ERRORS (2):

commands/bad.md:4
  Invalid YAML in frontmatter: mapping values are not allowed here

.mcp.json:5
  Invalid JSON: Expecting value at line 5 column 8
```

**JSON**:
```json
[
  {
    "file": "commands/bad.md",
    "line": 4,
    "error": "Invalid YAML in frontmatter: ..."
  }
]
```

## Script 2: inspect-components.py

### Purpose
Analyzes all components in your plugin and reports metadata and issues.

### Syntax
```bash
./scripts/inspect-components.py [OPTIONS] [PATH]
```

### Options
- `PATH`: Plugin directory (default: current directory)
- `--json`: Output results as JSON
- `--help`: Show help message

### What It Reports

**Component Information**:
- Name and file path
- Type (command, agent, skill)
- Description from frontmatter
- Version (if present)
- Any validation issues

**Counts**:
- Total components by type
- Components with issues
- Issues grouped by type

### Examples

```bash
# Inspect current plugin
./scripts/inspect-components.py

# Inspect specific plugin
./scripts/inspect-components.py /path/to/plugin

# JSON output with full details
./scripts/inspect-components.py --json

# Parse JSON output
./scripts/inspect-components.py --json | jq '.summary'
```

### Exit Codes
- `0`: Inspection completed (may have issues)
- `1`: Path doesn't exist or error occurred
- `2`: Script execution error

### Output Format

**Text (default)**:
```
=== Component Inspection Report ===

Total Components: 7
  Commands: 5
  Agents: 2

Components with Issues: 2

--- COMMANDS ---
✗ validate
  Path: commands/validate.md
  Description: Validate a plugin directory...
  Issues:
    - Missing required field: disable-model-invocation

✓ debug
  Path: commands/debug.md
  Description: Debug and fix plugin issues...
```

**JSON**:
```json
{
  "summary": {
    "total_components": 7,
    "by_type": {"command": 5, "agent": 2},
    "components_with_issues": 2
  },
  "components": [
    {
      "name": "validate",
      "path": "commands/validate.md",
      "type": "command",
      "metadata": {...},
      "issues": ["Missing required field: disable-model-invocation"]
    }
  ]
}
```

## Script 3: check-spec-compliance.py

### Purpose
Validates that your plugin complies with the official Claude Code specification.

### Syntax
```bash
./scripts/check-spec-compliance.py [OPTIONS] [PATH]
```

### Options
- `PATH`: Plugin directory (default: current directory)
- `--json`: Output results as JSON
- `--help`: Show help message

### What It Validates

**Required Fields by Type**:

Commands:
- `description`
- `allowed-tools`
- `argument-hint`
- `model` (sonnet, opus, haiku)
- `disable-model-invocation`

Agents:
- `description` (required, max 1024 chars)
- `tools` (optional, array)
- `model` (optional, sonnet/opus/haiku)

Skills:
- `name` (required, kebab-case)
- `description` (required, max 1024 chars)
- `allowed-tools` (optional)
- `version` (optional)
- `author` (optional)
- `tags` (optional)

**Deprecated Patterns**:
- HTML conditionals: `<IF>`, `<ELSE>`
- Pattern matching: `<MATCH>`
- Validation: `<VALIDATE>`

### Examples

```bash
# Check compliance
./scripts/check-spec-compliance.py

# Check specific plugin
./scripts/check-spec-compliance.py /path/to/plugin

# JSON output
./scripts/check-spec-compliance.py --json

# Check compliance status
./scripts/check-spec-compliance.py --json | jq '.compliant'
```

### Exit Codes
- `0`: Plugin is spec compliant
- `1`: Compliance issues found
- `2`: Script execution error

### Output Format

**Text (default)**:
```
=== Specification Compliance Report ===

ERRORS (5):

1. commands/create.md
   Type: missing_required_field
   Missing required command field: 'disable-model-invocation'.
   Reference: https://code.claude.com/docs/en/plugin-development

WARNINGS (2):

1. commands/old.md
   Type: deprecated_pattern
   Deprecated pattern detected: HTML IF conditional (<IF>).
   Migration: Remove HTML conditionals...
   Reference: https://code.claude.com/docs/en/plugin-development
```

**JSON**:
```json
{
  "compliant": false,
  "error_count": 5,
  "warning_count": 2,
  "errors": [
    {
      "type": "missing_required_field",
      "component": "commands/create.md",
      "message": "Missing required command field...",
      "reference": "https://code.claude.com/..."
    }
  ],
  "warnings": [...],
  "documentation": "https://code.claude.com/docs/en/plugin-development"
}
```

## Integration Patterns

### CI/CD Pipeline

**GitHub Actions**:
```yaml
name: Validate Plugin

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install pyyaml
      - run: ./scripts/check-formats.py
      - run: ./scripts/inspect-components.py
      - run: ./scripts/check-spec-compliance.py
```

### Pre-commit Hook

**.git/hooks/pre-commit**:
```bash
#!/bin/bash
set -e

echo "Checking formats..."
python scripts/check-formats.py || exit 1

echo "Checking spec compliance..."
python scripts/check-spec-compliance.py || exit 1

echo "✓ All checks passed"
```

### Manual Validation Workflow

```bash
# 1. Check format
./scripts/check-formats.py
if [ $? -ne 0 ]; then
  echo "Fix format errors and try again"
  exit 1
fi

# 2. Inspect components
./scripts/inspect-components.py
# Review any issues reported

# 3. Check compliance
./scripts/check-spec-compliance.py
if [ $? -ne 0 ]; then
  echo "Fix compliance issues"
  exit 1
fi

echo "✓ Plugin ready!"
```

## Migration Guide for Deprecated Patterns

### Pattern: HTML IF Conditional

**Deprecated**:
```markdown
<IF condition="debug">
  Debug information
</IF>
```

**Modern Approach**:
Handle the condition in your component logic or use environment configuration:

```markdown
For debugging, set the DEBUG environment variable.
Your component implementation checks this at runtime.
```

### Pattern: MATCH Statement

**Deprecated**:
```markdown
<MATCH expr="type">
  <CASE value="command">Command logic</CASE>
  <CASE value="agent">Agent logic</CASE>
</MATCH>
```

**Modern Approach**:
Implement pattern matching directly in your script:

```python
if component_type == "command":
    # handle command
elif component_type == "agent":
    # handle agent
```

### Pattern: VALIDATE Tag

**Deprecated**:
```markdown
<VALIDATE rule="required">
  Field content
</VALIDATE>
```

**Modern Approach**:
Use YAML frontmatter schema validation:

```yaml
---
description: "Valid description"
required-field: "value"
---
```

## Troubleshooting

### "PyYAML not installed"
```bash
pip install pyyaml
```

### "Permission denied"
```bash
chmod +x scripts/check-formats.py
chmod +x scripts/inspect-components.py
chmod +x scripts/check-spec-compliance.py
```

### Script runs slowly
- Ensure you're in the plugin directory
- Check for large binary files
- Scripts are optimized; typical run < 100ms

### JSON parsing errors in CI/CD
```bash
# Ensure json output flag is correct
./scripts/check-formats.py --json-output | jq .

# Don't forget --json-output (not just --json for format-checker)
```

## Performance Tips

1. Run scripts in correct order:
   - Format validation first (fastest)
   - Component inspection second
   - Spec compliance check last

2. Use `--json-only` for format checks if you only need JSON validation

3. For large plugin collections:
   ```bash
   for plugin in plugins/*; do
     ./scripts/check-spec-compliance.py "$plugin" --json
   done | jq -s 'map(select(.compliant == false))'
   ```

## Official References

- Plugin Development: https://code.claude.com/docs/en/plugin-development
- Command Specification: https://code.claude.com/docs/en/commands
- Agent Specification: https://code.claude.com/docs/en/agents
- Skill Specification: https://code.claude.com/docs/en/skills

## Support

For issues or improvements:
1. Check the script's `--help` output
2. Review official documentation
3. Check plugin example in this repository
4. Refer to test cases for usage examples
