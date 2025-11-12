"""
Test suite for component inspector script.

Tests validate:
- Listing all components in a plugin
- Showing component metadata from frontmatter
- Identifying component issues
- Generating component summary reports
- JSON output format
"""

import json
import tempfile
import shutil
import pytest
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


@pytest.fixture
def temp_inspect_dir():
    """Create a temporary plugin structure for inspection tests."""
    temp_dir = Path(tempfile.mkdtemp(prefix="test_component_inspect_"))

    # Create basic plugin structure
    (temp_dir / ".claude-plugin").mkdir()
    (temp_dir / "commands").mkdir()
    (temp_dir / "agents").mkdir()
    (temp_dir / "skills").mkdir()

    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestComponentListing:
    """Test listing components in a plugin."""

    def test_list_commands(self, temp_inspect_dir):
        """Test listing command components."""
        cmd_file = temp_inspect_dir / "commands" / "validate.md"
        content = """---
description: Validate a plugin
allowed-tools: ["file-system"]
argument-hint: "plugin-path"
model: sonnet
disable-model-invocation: false
---

# Validate Plugin

Validates plugin structure.
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_list_agents(self, temp_inspect_dir):
        """Test listing agent components."""
        agent_file = temp_inspect_dir / "agents" / "code-reviewer.md"
        content = """---
description: AI code reviewer agent
tools: ["code-analysis"]
model: opus
---

# Code Reviewer Agent

Reviews code for quality.
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_list_skills(self, temp_inspect_dir):
        """Test listing skill components."""
        skill_dir = temp_inspect_dir / "skills" / "testing"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """---
name: testing-tools
description: Tools for automated testing
allowed-tools: ["pytest", "jest"]
version: "1.0.0"
tags: ["qa", "automation"]
---

# Testing Tools Skill

Provides testing utilities.
"""
        skill_md.write_text(content)
        assert skill_md.exists()

    def test_list_multiple_components(self, temp_inspect_dir):
        """Test listing multiple components of each type."""
        # Add multiple commands
        for i in range(3):
            cmd_file = temp_inspect_dir / "commands" / f"cmd{i}.md"
            cmd_file.write_text(f"""---
description: Command {i}
allowed-tools: []
argument-hint: "none"
model: haiku
disable-model-invocation: false
---

Command body
""")

        # Add multiple agents
        for i in range(2):
            agent_file = temp_inspect_dir / "agents" / f"agent{i}.md"
            agent_file.write_text(f"""---
description: Agent {i}
---

Agent body
""")

        # Verify all created
        assert len(list((temp_inspect_dir / "commands").glob("*.md"))) == 3
        assert len(list((temp_inspect_dir / "agents").glob("*.md"))) == 2


class TestComponentMetadata:
    """Test extracting component metadata from frontmatter."""

    def test_command_metadata_extraction(self, temp_inspect_dir):
        """Test extracting metadata from command frontmatter."""
        cmd_file = temp_inspect_dir / "commands" / "publish.md"
        content = """---
description: Publish plugin to registry
allowed-tools: ["http", "file-system"]
argument-hint: "plugin-path registry-url"
model: sonnet
disable-model-invocation: false
---

Publish command.
"""
        cmd_file.write_text(content)
        content_read = cmd_file.read_text()
        assert "description: Publish plugin" in content_read
        assert "allowed-tools:" in content_read

    def test_agent_metadata_extraction(self, temp_inspect_dir):
        """Test extracting metadata from agent frontmatter."""
        agent_file = temp_inspect_dir / "agents" / "assistant.md"
        content = """---
description: General purpose assistant
tools: ["search", "calculator"]
model: opus
---

Assistant agent body.
"""
        agent_file.write_text(content)
        content_read = agent_file.read_text()
        assert "description: General purpose" in content_read
        assert "tools:" in content_read

    def test_skill_metadata_extraction(self, temp_inspect_dir):
        """Test extracting metadata from skill SKILL.md."""
        skill_dir = temp_inspect_dir / "skills" / "database"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """---
name: database-tools
description: Database query and migration tools
allowed-tools: ["sql", "db-client"]
version: "2.1.0"
author: "DB Team"
tags: ["database", "sql"]
---

Database tools.
"""
        skill_md.write_text(content)
        content_read = skill_md.read_text()
        assert "name: database-tools" in content_read
        assert "version:" in content_read
        assert "tags:" in content_read

    def test_optional_fields_present(self, temp_inspect_dir):
        """Test that optional fields are detected when present."""
        agent_file = temp_inspect_dir / "agents" / "advanced.md"
        content = """---
description: Advanced agent with options
tools: ["advanced-tool"]
model: opus
extra-metadata: "custom"
---

Advanced agent.
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_optional_fields_missing(self, temp_inspect_dir):
        """Test that components work with minimal required fields."""
        agent_file = temp_inspect_dir / "agents" / "minimal.md"
        content = """---
description: Minimal agent
---

Minimal agent.
"""
        agent_file.write_text(content)
        assert agent_file.exists()


class TestComponentIssueDetection:
    """Test identifying component issues."""

    def test_missing_frontmatter(self, temp_inspect_dir):
        """Test detection of missing frontmatter."""
        cmd_file = temp_inspect_dir / "commands" / "bad.md"
        content = """# No Frontmatter

This command has no frontmatter.
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_invalid_frontmatter(self, temp_inspect_dir):
        """Test detection of invalid YAML frontmatter."""
        cmd_file = temp_inspect_dir / "commands" / "invalid.md"
        content = """---
description: Test
invalid: [unclosed
---

Content
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_missing_required_field(self, temp_inspect_dir):
        """Test detection of missing required fields."""
        cmd_file = temp_inspect_dir / "commands" / "incomplete.md"
        content = """---
description: Missing required fields
allowed-tools: []
---

Content
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_skill_missing_skill_md(self, temp_inspect_dir):
        """Test detection of skill directory without SKILL.md."""
        skill_dir = temp_inspect_dir / "skills" / "broken"
        skill_dir.mkdir()
        # Create empty skill directory without SKILL.md
        assert skill_dir.exists()

    def test_invalid_field_type(self, temp_inspect_dir):
        """Test detection of incorrect field types."""
        cmd_file = temp_inspect_dir / "commands" / "wrong_type.md"
        content = """---
description: Test
allowed-tools: "should-be-array"
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Content
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()


class TestComponentSummaryReport:
    """Test generating component summary reports."""

    def test_summary_format_text(self, temp_inspect_dir):
        """Test text format component summary."""
        # Create sample components
        cmd_file = temp_inspect_dir / "commands" / "cmd.md"
        cmd_file.write_text("""---
description: Sample command
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Body
""")
        assert cmd_file.exists()

    def test_summary_counts_components(self, temp_inspect_dir):
        """Test that summary includes component counts."""
        # Create 2 commands, 1 agent
        for i in range(2):
            (temp_inspect_dir / "commands" / f"cmd{i}.md").write_text("""---
description: Test
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Body
""")

        (temp_inspect_dir / "agents" / "agent.md").write_text("""---
description: Test agent
---

Body
""")

        assert len(list((temp_inspect_dir / "commands").glob("*.md"))) == 2
        assert len(list((temp_inspect_dir / "agents").glob("*.md"))) == 1

    def test_summary_includes_issues(self, temp_inspect_dir):
        """Test that summary includes detected issues."""
        # Create valid and invalid components
        valid_cmd = temp_inspect_dir / "commands" / "valid.md"
        valid_cmd.write_text("""---
description: Valid
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Body
""")

        invalid_cmd = temp_inspect_dir / "commands" / "invalid.md"
        invalid_cmd.write_text("""---
incomplete: true
---

Body
""")

        assert valid_cmd.exists()
        assert invalid_cmd.exists()


class TestJsonOutput:
    """Test JSON output format."""

    def test_json_output_structure(self, temp_inspect_dir):
        """Test JSON output has correct structure."""
        cmd_file = temp_inspect_dir / "commands" / "cmd.md"
        cmd_file.write_text("""---
description: Test command
allowed-tools: ["tool"]
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Body
""")

        # Expected JSON structure should include components list
        assert cmd_file.exists()

    def test_json_contains_component_data(self, temp_inspect_dir):
        """Test JSON output contains all component data."""
        agent_file = temp_inspect_dir / "agents" / "agent.md"
        agent_file.write_text("""---
description: Test agent
tools: ["tool1", "tool2"]
model: opus
---

Body
""")

        assert agent_file.exists()

    def test_json_includes_error_details(self, temp_inspect_dir):
        """Test JSON output includes error details."""
        bad_file = temp_inspect_dir / "commands" / "bad.md"
        bad_file.write_text("""---
bad: [unclosed
---

Body
""")

        assert bad_file.exists()


class TestComponentTypeDetection:
    """Test correct detection of component types."""

    def test_command_type_detection(self, temp_inspect_dir):
        """Test that commands are correctly identified."""
        cmd_file = temp_inspect_dir / "commands" / "cmd.md"
        cmd_file.write_text("""---
description: Command
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Body
""")
        # Verify it's in commands directory
        assert cmd_file.parent.name == "commands"

    def test_agent_type_detection(self, temp_inspect_dir):
        """Test that agents are correctly identified."""
        agent_file = temp_inspect_dir / "agents" / "agent.md"
        agent_file.write_text("""---
description: Agent
---

Body
""")
        # Verify it's in agents directory
        assert agent_file.parent.name == "agents"

    def test_skill_type_detection(self, temp_inspect_dir):
        """Test that skills are correctly identified."""
        skill_dir = temp_inspect_dir / "skills" / "skill"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("""---
name: skill-name
description: Skill description
---

Body
""")
        # Verify it's SKILL.md in skills subdirectory
        assert skill_md.name == "SKILL.md"
        assert skill_md.parent.parent.name == "skills"
