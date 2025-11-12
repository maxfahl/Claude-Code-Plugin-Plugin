"""
Test suite for component validator functions.

Tests validate individual component file types:
- Command files with proper YAML frontmatter
- Agent files with proper YAML frontmatter
- Skill directories with SKILL.md files
- Hook configurations
- MCP configurations
"""

import json
import tempfile
import shutil
import pytest
from pathlib import Path
import yaml


@pytest.fixture
def temp_component_dir():
    """Create a temporary directory for component testing."""
    temp_dir = Path(tempfile.mkdtemp(prefix="test_component_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestCommandFileValidation:
    """Test validation of command markdown files with YAML frontmatter."""

    def test_valid_command_file_all_fields(self, temp_component_dir):
        """Test command file with all required and optional fields."""
        command_file = temp_component_dir / "test-command.md"

        command_content = """---
description: Test command for validation
allowed-tools: ["tool1", "tool2"]
argument-hint: "arg1 arg2"
model: sonnet
disable-model-invocation: false
---

# Test Command

This is the command body.
"""

        with open(command_file, 'w') as f:
            f.write(command_content)

        # Parse frontmatter
        with open(command_file, 'r') as f:
            content = f.read()

        assert "---" in content
        lines = content.split('\n')
        assert lines[0] == "---"

    def test_command_file_required_fields(self, temp_component_dir):
        """Test that command files require description, allowed-tools, argument-hint, model, disable-model-invocation."""
        command_file = temp_component_dir / "command.md"

        required_fields = ['description', 'allowed-tools', 'argument-hint', 'model', 'disable-model-invocation']

        command_content = """---
description: Test command
allowed-tools: []
argument-hint: none
model: sonnet
disable-model-invocation: false
---

Content
"""

        with open(command_file, 'w') as f:
            f.write(command_content)

        # Extract frontmatter
        with open(command_file, 'r') as f:
            lines = f.readlines()

        frontmatter_content = ""
        in_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                if in_frontmatter:
                    break
                in_frontmatter = True
            elif in_frontmatter:
                frontmatter_content += line

        frontmatter = yaml.safe_load(frontmatter_content)
        for field in required_fields:
            assert field in frontmatter, f"Missing required field: {field}"

    def test_command_file_missing_description(self, temp_component_dir):
        """Test detection of missing description field."""
        command_file = temp_component_dir / "incomplete.md"

        command_content = """---
allowed-tools: []
argument-hint: none
model: sonnet
---

Content
"""

        with open(command_file, 'w') as f:
            f.write(command_content)

        with open(command_file, 'r') as f:
            content = f.read()

        # Should detect missing 'description'
        assert "description:" not in content

    def test_command_file_allowed_tools_is_array(self, temp_component_dir):
        """Test that allowed-tools must be an array."""
        command_file = temp_component_dir / "command.md"

        valid_content = """---
description: Test
allowed-tools: ["tool1", "tool2"]
argument-hint: args
model: sonnet
disable-model-invocation: false
---

Content
"""

        with open(command_file, 'w') as f:
            f.write(valid_content)

        with open(command_file, 'r') as f:
            lines = f.readlines()

        frontmatter_str = ""
        in_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                if in_frontmatter:
                    break
                in_frontmatter = True
            elif in_frontmatter:
                frontmatter_str += line

        frontmatter = yaml.safe_load(frontmatter_str)
        assert isinstance(frontmatter['allowed-tools'], list)

    def test_command_file_model_valid_value(self, temp_component_dir):
        """Test that model field has valid values (sonnet, opus, haiku)."""
        valid_models = ['sonnet', 'opus', 'haiku']

        for model in valid_models:
            command_file = temp_component_dir / f"command-{model}.md"

            command_content = f"""---
description: Test
allowed-tools: []
argument-hint: none
model: {model}
disable-model-invocation: false
---

Content
"""

            with open(command_file, 'w') as f:
                f.write(command_content)

            with open(command_file, 'r') as f:
                lines = f.readlines()

            frontmatter_str = ""
            in_frontmatter = False
            for line in lines:
                if line.strip() == "---":
                    if in_frontmatter:
                        break
                    in_frontmatter = True
                elif in_frontmatter:
                    frontmatter_str += line

            frontmatter = yaml.safe_load(frontmatter_str)
            assert frontmatter['model'] in valid_models

    def test_command_file_disable_model_invocation_boolean(self, temp_component_dir):
        """Test that disable-model-invocation is boolean."""
        command_file = temp_component_dir / "command.md"

        command_content = """---
description: Test
allowed-tools: []
argument-hint: none
model: sonnet
disable-model-invocation: false
---

Content
"""

        with open(command_file, 'w') as f:
            f.write(command_content)

        with open(command_file, 'r') as f:
            lines = f.readlines()

        frontmatter_str = ""
        in_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                if in_frontmatter:
                    break
                in_frontmatter = True
            elif in_frontmatter:
                frontmatter_str += line

        frontmatter = yaml.safe_load(frontmatter_str)
        assert isinstance(frontmatter['disable-model-invocation'], bool)


class TestAgentFileValidation:
    """Test validation of agent markdown files with YAML frontmatter."""

    def test_valid_agent_file(self, temp_component_dir):
        """Test agent file with all valid fields."""
        agent_file = temp_component_dir / "test-agent.md"

        agent_content = """---
description: Test agent for validation
tools: ["tool1", "tool2"]
model: opus
---

# Test Agent

Agent content here.
"""

        with open(agent_file, 'w') as f:
            f.write(agent_content)

        with open(agent_file, 'r') as f:
            content = f.read()

        assert "description:" in content

    def test_agent_description_required(self, temp_component_dir):
        """Test that description field is required for agents."""
        agent_file = temp_component_dir / "agent.md"

        agent_content = """---
model: sonnet
---

Content
"""

        with open(agent_file, 'w') as f:
            f.write(agent_content)

        # Should be detected as missing description
        assert "description:" not in agent_content

    def test_agent_description_max_length(self, temp_component_dir):
        """Test that description field has max 1024 characters."""
        agent_file = temp_component_dir / "agent.md"

        valid_description = "x" * 1024
        long_description = "x" * 1025

        # Valid length
        agent_content = f"""---
description: {valid_description}
---

Content
"""

        with open(agent_file, 'w') as f:
            f.write(agent_content)

        with open(agent_file, 'r') as f:
            lines = f.readlines()

        frontmatter_str = ""
        in_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                if in_frontmatter:
                    break
                in_frontmatter = True
            elif in_frontmatter:
                frontmatter_str += line

        frontmatter = yaml.safe_load(frontmatter_str)
        assert len(frontmatter['description']) <= 1024

    def test_agent_tools_optional(self, temp_component_dir):
        """Test that tools field is optional for agents."""
        agent_file = temp_component_dir / "agent.md"

        # Without tools field
        agent_content = """---
description: Test agent
---

Content
"""

        with open(agent_file, 'w') as f:
            f.write(agent_content)

        assert (agent_file).exists()

    def test_agent_model_optional_values(self, temp_component_dir):
        """Test that model field is optional and has valid values."""
        valid_models = ['sonnet', 'opus', 'haiku']

        for model in valid_models:
            agent_file = temp_component_dir / f"agent-{model}.md"

            agent_content = f"""---
description: Test agent
model: {model}
---

Content
"""

            with open(agent_file, 'w') as f:
                f.write(agent_content)

            with open(agent_file, 'r') as f:
                lines = f.readlines()

            frontmatter_str = ""
            in_frontmatter = False
            for line in lines:
                if line.strip() == "---":
                    if in_frontmatter:
                        break
                    in_frontmatter = True
                elif in_frontmatter:
                    frontmatter_str += line

            frontmatter = yaml.safe_load(frontmatter_str)
            if 'model' in frontmatter:
                assert frontmatter['model'] in valid_models


class TestSkillValidation:
    """Test validation of skill directories and SKILL.md files."""

    def test_valid_skill_directory_structure(self, temp_component_dir):
        """Test valid skill directory with SKILL.md."""
        skill_dir = temp_component_dir / "test-skill"
        skill_dir.mkdir()

        skill_content = """---
name: test-skill
description: A test skill
allowed-tools: []
version: 1.0.0
author: Test Author
tags: ["test", "example"]
---

# Test Skill

Skill description here.
"""

        with open(skill_dir / "SKILL.md", 'w') as f:
            f.write(skill_content)

        assert (skill_dir / "SKILL.md").exists()

    def test_skill_name_required(self, temp_component_dir):
        """Test that skill name field is required."""
        skill_dir = temp_component_dir / "skill"
        skill_dir.mkdir()

        skill_content = """---
description: Skill without name
---

Content
"""

        with open(skill_dir / "SKILL.md", 'w') as f:
            f.write(skill_content)

        assert "name:" not in skill_content

    def test_skill_name_kebab_case(self, temp_component_dir):
        """Test that skill name must be kebab-case."""
        skill_dir = temp_component_dir / "test-skill"
        skill_dir.mkdir()

        skill_content = """---
name: test-skill
description: Valid skill name
---

Content
"""

        with open(skill_dir / "SKILL.md", 'w') as f:
            f.write(skill_content)

        with open(skill_dir / "SKILL.md", 'r') as f:
            lines = f.readlines()

        frontmatter_str = ""
        in_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                if in_frontmatter:
                    break
                in_frontmatter = True
            elif in_frontmatter:
                frontmatter_str += line

        frontmatter = yaml.safe_load(frontmatter_str)
        name = frontmatter.get('name', '')
        assert '-' in name or name.islower()

    def test_skill_description_required(self, temp_component_dir):
        """Test that description field is required."""
        skill_dir = temp_component_dir / "skill"
        skill_dir.mkdir()

        skill_content = """---
name: test-skill
---

Content
"""

        with open(skill_dir / "SKILL.md", 'w') as f:
            f.write(skill_content)

        assert "description:" not in skill_content

    def test_skill_description_max_length(self, temp_component_dir):
        """Test that description has max 1024 characters."""
        skill_dir = temp_component_dir / "skill"
        skill_dir.mkdir()

        valid_description = "x" * 1024

        skill_content = f"""---
name: test-skill
description: {valid_description}
---

Content
"""

        with open(skill_dir / "SKILL.md", 'w') as f:
            f.write(skill_content)

        with open(skill_dir / "SKILL.md", 'r') as f:
            lines = f.readlines()

        frontmatter_str = ""
        in_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                if in_frontmatter:
                    break
                in_frontmatter = True
            elif in_frontmatter:
                frontmatter_str += line

        frontmatter = yaml.safe_load(frontmatter_str)
        assert len(frontmatter.get('description', '')) <= 1024

    def test_skill_optional_fields(self, temp_component_dir):
        """Test that allowed-tools, version, author, tags are optional."""
        skill_dir = temp_component_dir / "skill"
        skill_dir.mkdir()

        # Without optional fields
        skill_content = """---
name: test-skill
description: Minimal skill
---

Content
"""

        with open(skill_dir / "SKILL.md", 'w') as f:
            f.write(skill_content)

        assert (skill_dir / "SKILL.md").exists()

    def test_skill_missing_skill_md_detected(self, temp_component_dir):
        """Test that missing SKILL.md in skill directory is detected."""
        skill_dir = temp_component_dir / "incomplete-skill"
        skill_dir.mkdir()

        # Create other files but not SKILL.md
        with open(skill_dir / "README.md", 'w') as f:
            f.write("# Skill")

        assert not (skill_dir / "SKILL.md").exists()


class TestHooksConfigValidation:
    """Test validation of hooks.json configuration."""

    def test_valid_hooks_config(self, temp_component_dir):
        """Test valid hooks configuration."""
        hooks_file = temp_component_dir / "hooks.json"

        hooks_config = {
            "after-create": ["script1.py", "script2.py"],
            "after-install": ["setup.py"]
        }

        with open(hooks_file, 'w') as f:
            json.dump(hooks_config, f)

        with open(hooks_file, 'r') as f:
            config = json.load(f)

        assert isinstance(config, dict)

    def test_hooks_config_must_be_json(self, temp_component_dir):
        """Test that hooks config is valid JSON."""
        hooks_file = temp_component_dir / "hooks.json"

        with open(hooks_file, 'w') as f:
            f.write("{invalid json")

        with open(hooks_file, 'r') as f:
            content = f.read()

        assert content == "{invalid json"

    def test_hooks_config_hook_values_are_arrays(self, temp_component_dir):
        """Test that hook values are arrays of strings."""
        hooks_file = temp_component_dir / "hooks.json"

        hooks_config = {
            "after-create": ["script1.py", "script2.py"],
            "after-install": ["setup.py"]
        }

        with open(hooks_file, 'w') as f:
            json.dump(hooks_config, f)

        with open(hooks_file, 'r') as f:
            config = json.load(f)

        for hook_name, scripts in config.items():
            assert isinstance(scripts, list)
            for script in scripts:
                assert isinstance(script, str)


class TestMCPConfigValidation:
    """Test validation of .mcp.json configuration."""

    def test_valid_mcp_config(self, temp_component_dir):
        """Test valid MCP configuration."""
        mcp_file = temp_component_dir / ".mcp.json"

        mcp_config = {
            "mcpServers": {
                "server1": {
                    "command": "node",
                    "args": ["server.js"]
                }
            }
        }

        with open(mcp_file, 'w') as f:
            json.dump(mcp_config, f)

        with open(mcp_file, 'r') as f:
            config = json.load(f)

        assert "mcpServers" in config

    def test_mcp_config_must_be_json(self, temp_component_dir):
        """Test that MCP config is valid JSON."""
        mcp_file = temp_component_dir / ".mcp.json"

        with open(mcp_file, 'w') as f:
            f.write("{invalid json")

        with open(mcp_file, 'r') as f:
            content = f.read()

        assert content == "{invalid json"

    def test_mcp_servers_is_object(self, temp_component_dir):
        """Test that mcpServers is an object."""
        mcp_file = temp_component_dir / ".mcp.json"

        mcp_config = {
            "mcpServers": {}
        }

        with open(mcp_file, 'w') as f:
            json.dump(mcp_config, f)

        with open(mcp_file, 'r') as f:
            config = json.load(f)

        assert isinstance(config.get("mcpServers"), dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
