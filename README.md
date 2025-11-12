<div align="center">

# 🔌 Max Fahl's Claude Code Plugins

**A curated collection of high-quality Claude Code plugins for enhanced development workflows**

[![Plugins](https://img.shields.io/badge/plugins-1-blue?style=for-the-badge)](https://github.com/maxfahl/maxfahl-claude-market-place)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen?style=for-the-badge)](https://github.com/maxfahl/maxfahl-claude-market-place)

[Installation](#-installation) • [Plugins](#-available-plugins) • [Contributing](#-contributing) • [Support](#-support)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Installation](#-installation)
- [Available Plugins](#-available-plugins)
- [Why Use This Marketplace](#-why-use-this-marketplace)
- [Adding Plugins](#-adding-more-plugins)
- [Contributing](#-contributing)
- [Support](#-support)
- [License](#-license)

---

## 🎯 About

This marketplace provides professionally maintained Claude Code plugins that enhance your development workflow. Each plugin is:

- ✅ **Thoroughly tested** with comprehensive test coverage
- ✅ **Well documented** with usage examples and guides
- ✅ **Actively maintained** with regular updates
- ✅ **Specification compliant** following official Anthropic guidelines
- ✅ **Production ready** with robust error handling

---

## 🚀 Installation

### Quick Start

Add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add maxfahl/maxfahl-claude-market-place
```

That's it! You can now browse and install any plugin from this collection.

### Manual Installation

If you prefer to install individual plugins manually:

1. Navigate to your Claude Code plugins directory:
   ```bash
   cd ~/.claude/plugins
   ```

2. Clone the marketplace repository:
   ```bash
   git clone https://github.com/maxfahl/maxfahl-claude-market-place.git marketplace-maxfahl
   ```

3. Restart Claude Code to load the plugins

---

## 🔧 Available Plugins

### cc-plugins

<div align="left">

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/maxfahl/maxfahl-claude-market-place)
[![Tests](https://img.shields.io/badge/tests-413%20passing-brightgreen)](https://github.com/maxfahl/maxfahl-claude-market-place)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)](https://github.com/maxfahl/maxfahl-claude-market-place)

</div>

**A comprehensive meta-plugin for creating, validating, and maintaining Claude Code plugins**

Perfect for plugin developers who want to streamline their workflow and ensure their plugins meet official specifications.

#### 📦 Installation

```bash
/plugin install cc-plugins@maxfahl
```

#### ✨ Features

- **🛠️ Plugin Scaffolding** - Generate new plugins with correct structure
- **✅ Validation Tools** - Validate against official Claude Code specifications
- **🐛 Debugging Utilities** - Identify and fix common plugin issues
- **📝 Documentation Generation** - Auto-generate comprehensive docs
- **🤖 AI Agents** - 3 specialized agents for architecture, debugging, and documentation
- **🎓 Development Skills** - 2 skills for plugin creation and validation guidance
- **📋 5 Commands** - Complete toolkit for plugin development lifecycle

#### 📚 What You Get

| Component | Count | Description |
|-----------|-------|-------------|
| Commands | 5 | `/create`, `/validate`, `/update`, `/document`, `/debug` |
| Agents | 3 | Architecture, debugging, documentation specialists |
| Skills | 2 | Plugin development and validation expertise |
| Scripts | 6 | Validation, scaffolding, format checking |
| Templates | 5 | Ready-to-use component templates |
| Tests | 413 | Comprehensive test coverage (98%) |

#### 🎯 Quick Example

```bash
# Create a new plugin
/cc-plugins:create my-awesome-plugin

# Validate it
/cc-plugins:validate my-awesome-plugin

# Generate documentation
/cc-plugins:document my-awesome-plugin

# Debug any issues
/cc-plugins:debug my-awesome-plugin
```

#### 🔗 Links

- 📖 [Full Documentation](./plugins/cc-plugins/README.md)
- 📘 [User Guide](./plugins/cc-plugins/docs/user-guide.md)
- 👨‍💻 [Developer Guide](./plugins/cc-plugins/docs/developer-guide.md)
- 🔍 [API Reference](./plugins/cc-plugins/docs/api-reference.md)

---

## 💡 Why Use This Marketplace?

### 🎯 Quality Assurance

Every plugin in this marketplace undergoes:
- Comprehensive testing (98%+ coverage)
- Code review and quality checks
- Documentation verification
- Specification compliance validation

### 🚀 Easy Updates

Stay up-to-date effortlessly:

```bash
/plugin update
```

All your installed plugins will automatically update to the latest versions.

### 🤝 Community Driven

- **Open Issues**: [Report bugs or request features](https://github.com/maxfahl/maxfahl-claude-market-place/issues)
- **Contributions Welcome**: Submit your own plugins
- **Active Maintenance**: Regular updates and improvements
- **Responsive Support**: Get help when you need it

### 📦 Growing Collection

More plugins coming soon! This marketplace will expand with:
- Workflow automation plugins
- Code quality tools
- Development utilities
- Integration helpers

---

## 🔨 Adding More Plugins

Want to add your plugin to this marketplace? Here's how:

### For Plugin Authors

1. **Fork this repository**
2. **Add your plugin** to the `plugins/` directory
3. **Update** `.claude-plugin/marketplace.json` with your plugin details:

```json
{
  "name": "your-plugin-name",
  "source": "./plugins/your-plugin-name",
  "description": "What your plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "url": "https://github.com/yourusername"
  },
  "category": "Development Engineering",
  "homepage": "https://github.com/maxfahl/claude-plugins/tree/main/plugins/your-plugin-name",
  "keywords": ["keyword1", "keyword2"]
}
```

4. **Submit a pull request** with your changes

### Plugin Requirements

To be included, plugins must:
- ✅ Follow official Claude Code plugin specifications
- ✅ Include comprehensive documentation
- ✅ Have a test suite (preferred)
- ✅ Use semantic versioning
- ✅ Have a valid MIT-compatible license

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs** - Open an issue describing the problem
- 💡 **Request Features** - Suggest new plugins or improvements
- 📝 **Improve Documentation** - Fix typos, clarify instructions
- 🔧 **Submit Plugins** - Share your own plugins with the community
- ⭐ **Star This Repo** - Show your support!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/maxfahl/maxfahl-claude-market-place.git
cd maxfahl-claude-market-place

# Make your changes
# ...

# Commit and push
git add .
git commit -m "Description of changes"
git push origin your-branch

# Open a pull request
```

### Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

---

## 📞 Support

### Get Help

- 📖 **Documentation** - Check the [plugin docs](./plugins/)
- 🐛 **Issues** - [Report bugs](https://github.com/maxfahl/maxfahl-claude-market-place/issues)
- 💬 **Discussions** - [Ask questions](https://github.com/maxfahl/maxfahl-claude-market-place/discussions)
- 🌐 **Website** - [maxfahl.com](https://maxfahl.com)

### Stay Connected

- 🐦 **Twitter** - [@maxfahl](https://twitter.com/maxfahl)
- 💼 **LinkedIn** - [Max Fahl](https://linkedin.com/in/maxfahl)
- 🔗 **GitHub** - [@maxfahl](https://github.com/maxfahl)

---

## 📄 License

This marketplace and included plugins are licensed under the [MIT License](LICENSE).

Individual plugins may have their own licenses - see each plugin's directory for details.

---

## 🙏 Acknowledgments

- **Anthropic** - For creating Claude Code and the plugin system
- **Community** - For feedback, contributions, and support
- **Plugin Developers** - For sharing their tools with the community

---

<div align="center">

**[⬆ back to top](#-max-fahls-claude-code-plugins)**

Made with ❤️ by [Max Fahl](https://maxfahl.com)

[![GitHub](https://img.shields.io/badge/GitHub-maxfahl-black?style=for-the-badge&logo=github)](https://github.com/maxfahl)
[![Website](https://img.shields.io/badge/Website-maxfahl.com-blue?style=for-the-badge&logo=google-chrome)](https://maxfahl.com)

</div>
