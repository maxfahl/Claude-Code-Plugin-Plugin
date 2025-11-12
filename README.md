# Max Fahl's Claude Code Plugins

Curated collection of Claude Code plugins.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add maxfahl/claude-plugins
```

## Available Plugins

### cc-plugins

Meta-plugin for creating, validating, and maintaining Claude Code plugins.

**Install:**
```bash
/plugin install cc-plugins@maxfahl
```

**Features:**
- Plugin scaffolding with official specifications
- Comprehensive validation tools
- Debugging utilities
- Documentation generation
- 5 commands, 3 agents, 2 skills
- 413 tests with 98% coverage

[Full Documentation](./plugins/cc-plugins/README.md)

## Adding Plugins

To add more plugins to this marketplace:

1. Create symlink: `cd plugins && ln -s ~/.claude/plugins/my-plugin my-plugin`
2. Update `.claude-plugin/marketplace.json`
3. Commit and push

## License

MIT License - See individual plugin directories for specific licenses.

---

Maintained by Max Fahl
