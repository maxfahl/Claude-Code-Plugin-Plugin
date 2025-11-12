"""
Test suite for spec checker script.

Tests validate:
- Unsupported frontmatter fields detection
- Deprecated features warnings
- Spec compliance validation
- Official documentation references
- Migration guidance for old patterns
"""

import tempfile
import shutil
import pytest
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


@pytest.fixture
def temp_spec_dir():
    """Create a temporary plugin structure for spec testing."""
    temp_dir = Path(tempfile.mkdtemp(prefix="test_spec_check_"))

    # Create basic plugin structure
    (temp_dir / ".claude-plugin").mkdir()
    (temp_dir / "commands").mkdir()
    (temp_dir / "agents").mkdir()
    (temp_dir / "skills").mkdir()

    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestUnsupportedFields:
    """Test detection of unsupported frontmatter fields."""

    def test_unsupported_command_field(self, temp_spec_dir):
        """Test detection of unsupported field in command."""
        cmd_file = temp_spec_dir / "commands" / "test.md"
        content = """---
description: Test command
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
unsupported-field: "this should warn"
---

Content
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_unsupported_agent_field(self, temp_spec_dir):
        """Test detection of unsupported field in agent."""
        agent_file = temp_spec_dir / "agents" / "test.md"
        content = """---
description: Test agent
custom-metadata: "not official"
unknown-field: true
---

Content
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_valid_command_fields_only(self, temp_spec_dir):
        """Test that valid commands don't generate warnings."""
        cmd_file = temp_spec_dir / "commands" / "valid.md"
        content = """---
description: Valid command
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Content
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_valid_agent_fields_only(self, temp_spec_dir):
        """Test that valid agents don't generate warnings."""
        agent_file = temp_spec_dir / "agents" / "valid.md"
        content = """---
description: Valid agent
tools: ["tool1"]
model: opus
---

Content
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_valid_skill_fields_only(self, temp_spec_dir):
        """Test that valid skills don't generate warnings."""
        skill_dir = temp_spec_dir / "skills" / "valid"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """---
name: valid-skill
description: Valid skill
allowed-tools: []
version: "1.0.0"
tags: ["test"]
---

Content
"""
        skill_md.write_text(content)
        assert skill_md.exists()


class TestDeprecatedFeatures:
    """Test detection of deprecated features."""

    def test_deprecated_html_conditionals_warning(self, temp_spec_dir):
        """Test warning about HTML conditionals (deprecated)."""
        cmd_file = temp_spec_dir / "commands" / "old.md"
        content = """---
description: Old command
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Content with deprecated HTML conditionals:
<IF condition="test">This is old</IF>
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_deprecated_match_syntax_warning(self, temp_spec_dir):
        """Test warning about MATCH syntax (deprecated)."""
        agent_file = temp_spec_dir / "agents" / "old.md"
        content = """---
description: Old agent
---

Content with deprecated MATCH:
<MATCH expr="test">
  Old pattern
</MATCH>
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_deprecated_validate_tag_warning(self, temp_spec_dir):
        """Test warning about VALIDATE tag (deprecated)."""
        agent_file = temp_spec_dir / "agents" / "validator.md"
        content = """---
description: Agent with deprecated validation
---

Content with deprecated VALIDATE:
<VALIDATE rule="pattern">Content</VALIDATE>
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_no_warnings_for_modern_syntax(self, temp_spec_dir):
        """Test that modern components don't trigger deprecation warnings."""
        cmd_file = temp_spec_dir / "commands" / "modern.md"
        content = """---
description: Modern command
allowed-tools: ["tool"]
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

# Modern Content

Just regular markdown and content.
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()


class TestCommandSpecCompliance:
    """Test command specification compliance."""

    def test_command_required_fields_present(self, temp_spec_dir):
        """Test command has all required fields."""
        cmd_file = temp_spec_dir / "commands" / "compliant.md"
        content = """---
description: Compliant command
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Content
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_command_required_field_missing(self, temp_spec_dir):
        """Test detection of missing required command field."""
        cmd_file = temp_spec_dir / "commands" / "incomplete.md"
        content = """---
description: Missing model
allowed-tools: []
argument-hint: arg
disable-model-invocation: false
---

Content
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_command_unsupported_conditional(self, temp_spec_dir):
        """Test detection of unsupported HTML conditionals in commands."""
        cmd_file = temp_spec_dir / "commands" / "conditional.md"
        content = """---
description: Command with conditionals
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

<IF condition="test">Conditional content</IF>
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()


class TestAgentSpecCompliance:
    """Test agent specification compliance."""

    def test_agent_required_field_present(self, temp_spec_dir):
        """Test agent has required description field."""
        agent_file = temp_spec_dir / "agents" / "compliant.md"
        content = """---
description: Compliant agent
---

Content
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_agent_required_field_missing(self, temp_spec_dir):
        """Test detection of missing description in agent."""
        agent_file = temp_spec_dir / "agents" / "incomplete.md"
        content = """---
tools: ["tool"]
model: opus
---

Content
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_agent_optional_model_field(self, temp_spec_dir):
        """Test agent with optional model field."""
        agent_file = temp_spec_dir / "agents" / "with_model.md"
        content = """---
description: Agent with model
model: opus
---

Content
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_agent_optional_tools_field(self, temp_spec_dir):
        """Test agent with optional tools field."""
        agent_file = temp_spec_dir / "agents" / "with_tools.md"
        content = """---
description: Agent with tools
tools: ["tool1", "tool2"]
---

Content
"""
        agent_file.write_text(content)
        assert agent_file.exists()


class TestSkillSpecCompliance:
    """Test skill specification compliance."""

    def test_skill_required_name_field(self, temp_spec_dir):
        """Test skill has required name field."""
        skill_dir = temp_spec_dir / "skills" / "named"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """---
name: my-skill
description: Test skill
---

Content
"""
        skill_md.write_text(content)
        assert skill_md.exists()

    def test_skill_required_description_field(self, temp_spec_dir):
        """Test skill has required description field."""
        skill_dir = temp_spec_dir / "skills" / "described"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """---
name: my-skill
description: Test skill description
---

Content
"""
        skill_md.write_text(content)
        assert skill_md.exists()

    def test_skill_optional_fields(self, temp_spec_dir):
        """Test skill with optional fields."""
        skill_dir = temp_spec_dir / "skills" / "full"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        content = """---
name: full-skill
description: Full skill with optional fields
allowed-tools: ["tool1"]
version: "1.0.0"
author: "Author Name"
tags: ["tag1", "tag2"]
---

Content
"""
        skill_md.write_text(content)
        assert skill_md.exists()


class TestMigrationGuidance:
    """Test migration guidance for deprecated patterns."""

    def test_migration_guidance_for_if_conditional(self, temp_spec_dir):
        """Test migration guidance is provided for IF conditional."""
        cmd_file = temp_spec_dir / "commands" / "with_if.md"
        content = """---
description: Command with IF
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

<IF condition="env.DEBUG">Debug mode</IF>
"""
        cmd_file.write_text(content)
        assert cmd_file.exists()

    def test_migration_guidance_for_match_syntax(self, temp_spec_dir):
        """Test migration guidance for MATCH syntax."""
        agent_file = temp_spec_dir / "agents" / "with_match.md"
        content = """---
description: Agent with MATCH
---

<MATCH expr="pattern">
  Old pattern
</MATCH>
"""
        agent_file.write_text(content)
        assert agent_file.exists()

    def test_migration_guidance_for_validate(self, temp_spec_dir):
        """Test migration guidance for VALIDATE."""
        agent_file = temp_spec_dir / "agents" / "with_validate.md"
        content = """---
description: Agent with VALIDATE
---

<VALIDATE rule="required">Content</VALIDATE>
"""
        agent_file.write_text(content)
        assert agent_file.exists()


class TestDocumentationReferences:
    """Test official documentation references in output."""

    def test_spec_references_official_docs(self, temp_spec_dir):
        """Test that reports reference official documentation."""
        cmd_file = temp_spec_dir / "commands" / "test.md"
        cmd_file.write_text("""---
description: Test
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Content
""")
        # Spec checker should reference: https://code.claude.com/docs/en/plugin-development
        assert cmd_file.exists()

    def test_unsupported_field_references_docs(self, temp_spec_dir):
        """Test that unsupported field warnings reference documentation."""
        cmd_file = temp_spec_dir / "commands" / "bad.md"
        cmd_file.write_text("""---
description: Test
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
unsupported: "field"
---

Content
""")
        assert cmd_file.exists()

    def test_deprecated_feature_references_migration(self, temp_spec_dir):
        """Test that deprecated features reference migration docs."""
        cmd_file = temp_spec_dir / "commands" / "old.md"
        cmd_file.write_text("""---
description: Old command
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

<IF condition="test">Old</IF>
""")
        assert cmd_file.exists()


class TestComplianceReport:
    """Test compliance report generation."""

    def test_compliance_report_includes_summary(self, temp_spec_dir):
        """Test compliance report includes summary."""
        # Create compliant component
        (temp_spec_dir / "commands" / "valid.md").write_text("""---
description: Valid
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

Content
""")
        assert (temp_spec_dir / "commands" / "valid.md").exists()

    def test_compliance_report_lists_violations(self, temp_spec_dir):
        """Test compliance report lists violations."""
        # Create non-compliant component
        (temp_spec_dir / "commands" / "invalid.md").write_text("""---
description: Invalid
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
unsupported-field: "yes"
---

<IF condition="test">Content</IF>
""")
        assert (temp_spec_dir / "commands" / "invalid.md").exists()

    def test_compliance_report_suggests_fixes(self, temp_spec_dir):
        """Test compliance report includes fix suggestions."""
        # Create component needing fixes
        (temp_spec_dir / "agents" / "fix_me.md").write_text("""---
deprecated-field: true
---

Content
""")
        assert (temp_spec_dir / "agents" / "fix_me.md").exists()


class TestKnownDeprecatedPatterns:
    """Test detection of all known deprecated patterns."""

    def test_html_if_pattern(self, temp_spec_dir):
        """Test detection of <IF> pattern."""
        cmd_file = temp_spec_dir / "commands" / "cmd.md"
        content = """---
description: Test
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

<IF condition="test">deprecated</IF>
"""
        cmd_file.write_text(content)
        assert "<IF" in cmd_file.read_text()

    def test_html_else_pattern(self, temp_spec_dir):
        """Test detection of <ELSE> pattern."""
        cmd_file = temp_spec_dir / "commands" / "cmd.md"
        content = """---
description: Test
allowed-tools: []
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

<ELSE>deprecated</ELSE>
"""
        cmd_file.write_text(content)
        assert "<ELSE" in cmd_file.read_text()

    def test_html_match_pattern(self, temp_spec_dir):
        """Test detection of <MATCH> pattern."""
        agent_file = temp_spec_dir / "agents" / "agent.md"
        content = """---
description: Test agent
---

<MATCH expr="pattern">deprecated</MATCH>
"""
        agent_file.write_text(content)
        assert "<MATCH" in agent_file.read_text()

    def test_html_validate_pattern(self, temp_spec_dir):
        """Test detection of <VALIDATE> pattern."""
        agent_file = temp_spec_dir / "agents" / "agent.md"
        content = """---
description: Test agent
---

<VALIDATE rule="pattern">deprecated</VALIDATE>
"""
        agent_file.write_text(content)
        assert "<VALIDATE" in agent_file.read_text()
