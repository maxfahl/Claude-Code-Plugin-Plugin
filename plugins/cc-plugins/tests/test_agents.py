"""
Test suite for cc-plugins agents.

Tests ensure that all agents:
- Have valid YAML frontmatter
- Include trigger-rich descriptions (max 1024 chars)
- Specify appropriate tools
- Follow Claude Code agent specification
- Are properly formatted
"""

import os
import json
import pytest
import yaml
from pathlib import Path


@pytest.fixture
def plugin_root():
    """Returns the path to the cc-plugins plugin root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def agents_dir(plugin_root):
    """Returns the path to the agents directory."""
    return plugin_root / "agents"


class TestPluginArchitectAgent:
    """Test suite for plugin-architect agent."""

    def test_plugin_architect_file_exists(self, agents_dir):
        """Test that plugin-architect.md agent file exists."""
        agent_file = agents_dir / "plugin-architect.md"
        assert agent_file.exists(), f"plugin-architect.md does not exist at {agent_file}"
        assert agent_file.is_file(), f"plugin-architect.md is not a file"

    def test_plugin_architect_has_frontmatter(self, agents_dir):
        """Test that plugin-architect.md has YAML frontmatter."""
        agent_file = agents_dir / "plugin-architect.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Agent should start with frontmatter delimiter ---"
        assert "---" in content[3:], "Agent should have closing frontmatter delimiter ---"

    def test_plugin_architect_frontmatter_valid(self, agents_dir):
        """Test that plugin-architect.md has valid YAML frontmatter."""
        agent_file = agents_dir / "plugin-architect.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        # Extract frontmatter
        parts = content.split("---", 2)
        assert len(parts) >= 3, "Frontmatter should be properly delimited"

        frontmatter_str = parts[1].strip()
        frontmatter = yaml.safe_load(frontmatter_str)

        assert frontmatter is not None, "Frontmatter should be valid YAML"
        assert "description" in frontmatter, "Frontmatter must include 'description'"

    def test_plugin_architect_description_length(self, agents_dir):
        """Test that plugin-architect description is within 1024 character limit."""
        agent_file = agents_dir / "plugin-architect.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "")

        assert len(description) <= 1024, \
            f"Description must be max 1024 characters, got {len(description)}"

    def test_plugin_architect_has_trigger_keywords(self, agents_dir):
        """Test that plugin-architect description includes activation triggers."""
        agent_file = agents_dir / "plugin-architect.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "").lower()

        # Should mention when to use this agent
        trigger_keywords = ["architecture", "design", "structure", "pattern", "review"]
        has_trigger = any(keyword in description for keyword in trigger_keywords)
        assert has_trigger, "Description should include architectural trigger keywords"

    def test_plugin_architect_has_tools(self, agents_dir):
        """Test that plugin-architect specifies appropriate tools."""
        agent_file = agents_dir / "plugin-architect.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())

        # Tools are optional, but if specified should include Read at minimum
        if "tools" in frontmatter:
            tools = frontmatter["tools"]
            assert isinstance(tools, list), "Tools should be a list"
            assert "Read" in tools, "Should include Read tool for reviewing code"


class TestPluginDebuggerAgent:
    """Test suite for plugin-debugger agent."""

    def test_plugin_debugger_file_exists(self, agents_dir):
        """Test that plugin-debugger.md agent file exists."""
        agent_file = agents_dir / "plugin-debugger.md"
        assert agent_file.exists(), f"plugin-debugger.md does not exist at {agent_file}"
        assert agent_file.is_file(), f"plugin-debugger.md is not a file"

    def test_plugin_debugger_has_frontmatter(self, agents_dir):
        """Test that plugin-debugger.md has YAML frontmatter."""
        agent_file = agents_dir / "plugin-debugger.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Agent should start with frontmatter"
        assert "---" in content[3:], "Agent should have closing frontmatter"

    def test_plugin_debugger_frontmatter_valid(self, agents_dir):
        """Test that plugin-debugger.md has valid YAML frontmatter."""
        agent_file = agents_dir / "plugin-debugger.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        assert len(parts) >= 3, "Frontmatter should be properly delimited"

        frontmatter_str = parts[1].strip()
        frontmatter = yaml.safe_load(frontmatter_str)

        assert frontmatter is not None, "Frontmatter should be valid YAML"
        assert "description" in frontmatter, "Frontmatter must include 'description'"

    def test_plugin_debugger_description_length(self, agents_dir):
        """Test that plugin-debugger description is within 1024 character limit."""
        agent_file = agents_dir / "plugin-debugger.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "")

        assert len(description) <= 1024, \
            f"Description must be max 1024 characters, got {len(description)}"

    def test_plugin_debugger_has_trigger_keywords(self, agents_dir):
        """Test that plugin-debugger description includes debugging triggers."""
        agent_file = agents_dir / "plugin-debugger.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "").lower()

        # Should mention debugging, errors, fixes
        trigger_keywords = ["debug", "error", "fix", "issue", "validation", "problem"]
        has_trigger = any(keyword in description for keyword in trigger_keywords)
        assert has_trigger, "Description should include debugging trigger keywords"

    def test_plugin_debugger_has_bash_tool(self, agents_dir):
        """Test that plugin-debugger includes Bash tool for running validation."""
        agent_file = agents_dir / "plugin-debugger.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())

        if "tools" in frontmatter:
            tools = frontmatter["tools"]
            assert "Bash" in tools, "Should include Bash tool for running validation scripts"


class TestPluginDocumenterAgent:
    """Test suite for plugin-documenter agent."""

    def test_plugin_documenter_file_exists(self, agents_dir):
        """Test that plugin-documenter.md agent file exists."""
        agent_file = agents_dir / "plugin-documenter.md"
        assert agent_file.exists(), f"plugin-documenter.md does not exist at {agent_file}"
        assert agent_file.is_file(), f"plugin-documenter.md is not a file"

    def test_plugin_documenter_has_frontmatter(self, agents_dir):
        """Test that plugin-documenter.md has YAML frontmatter."""
        agent_file = agents_dir / "plugin-documenter.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Agent should start with frontmatter"
        assert "---" in content[3:], "Agent should have closing frontmatter"

    def test_plugin_documenter_frontmatter_valid(self, agents_dir):
        """Test that plugin-documenter.md has valid YAML frontmatter."""
        agent_file = agents_dir / "plugin-documenter.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        assert len(parts) >= 3, "Frontmatter should be properly delimited"

        frontmatter_str = parts[1].strip()
        frontmatter = yaml.safe_load(frontmatter_str)

        assert frontmatter is not None, "Frontmatter should be valid YAML"
        assert "description" in frontmatter, "Frontmatter must include 'description'"

    def test_plugin_documenter_description_length(self, agents_dir):
        """Test that plugin-documenter description is within 1024 character limit."""
        agent_file = agents_dir / "plugin-documenter.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "")

        assert len(description) <= 1024, \
            f"Description must be max 1024 characters, got {len(description)}"

    def test_plugin_documenter_has_trigger_keywords(self, agents_dir):
        """Test that plugin-documenter description includes documentation triggers."""
        agent_file = agents_dir / "plugin-documenter.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "").lower()

        # Should mention documentation, readme, guides
        trigger_keywords = ["document", "readme", "guide", "api", "usage"]
        has_trigger = any(keyword in description for keyword in trigger_keywords)
        assert has_trigger, "Description should include documentation trigger keywords"

    def test_plugin_documenter_has_write_tool(self, agents_dir):
        """Test that plugin-documenter includes Write tool for creating docs."""
        agent_file = agents_dir / "plugin-documenter.md"
        with open(agent_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())

        if "tools" in frontmatter:
            tools = frontmatter["tools"]
            assert "Write" in tools, "Should include Write tool for creating documentation"


class TestAgentFrontmatterFormat:
    """Test frontmatter format compliance across all agents."""

    def test_all_agents_have_description(self, agents_dir):
        """Test that all agents have description in frontmatter."""
        agent_files = list(agents_dir.glob("*.md"))
        assert len(agent_files) >= 3, "Should have at least 3 agent files"

        for agent_file in agent_files:
            with open(agent_file, 'r') as f:
                content = f.read()

            parts = content.split("---", 2)
            assert len(parts) >= 3, f"{agent_file.name} should have frontmatter"

            frontmatter = yaml.safe_load(parts[1].strip())
            assert "description" in frontmatter, \
                f"{agent_file.name} must have 'description' in frontmatter"

    def test_all_agents_frontmatter_properly_closed(self, agents_dir):
        """Test that all agents have properly closed frontmatter."""
        agent_files = list(agents_dir.glob("*.md"))

        for agent_file in agent_files:
            with open(agent_file, 'r') as f:
                content = f.read()

            assert content.startswith("---"), \
                f"{agent_file.name} should start with ---"

            # Should have at least 2 occurrences of ---
            assert content.count("---") >= 2, \
                f"{agent_file.name} should have closing ---"

    def test_all_agents_have_content_after_frontmatter(self, agents_dir):
        """Test that all agents have content after frontmatter."""
        agent_files = list(agents_dir.glob("*.md"))

        for agent_file in agent_files:
            with open(agent_file, 'r') as f:
                content = f.read()

            parts = content.split("---", 2)
            assert len(parts) >= 3, f"{agent_file.name} should have content after frontmatter"

            body = parts[2].strip()
            assert len(body) > 0, \
                f"{agent_file.name} should have content after frontmatter"
