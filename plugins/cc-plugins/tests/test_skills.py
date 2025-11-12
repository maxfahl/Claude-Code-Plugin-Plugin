"""
Test suite for cc-plugins skills.

Tests ensure that all skills:
- Have valid YAML frontmatter with 'name' and 'description'
- Include trigger-rich descriptions (max 1024 chars)
- Follow progressive disclosure pattern
- Are properly formatted
- Include supporting documentation
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
def skills_dir(plugin_root):
    """Returns the path to the skills directory."""
    return plugin_root / "skills"


class TestPluginDevelopmentSkill:
    """Test suite for plugin-development skill."""

    def test_plugin_development_skill_dir_exists(self, skills_dir):
        """Test that plugin-development skill directory exists."""
        skill_dir = skills_dir / "plugin-development"
        assert skill_dir.exists(), f"plugin-development directory does not exist"
        assert skill_dir.is_dir(), f"plugin-development is not a directory"

    def test_plugin_development_skill_file_exists(self, skills_dir):
        """Test that plugin-development/SKILL.md file exists."""
        skill_file = skills_dir / "plugin-development" / "SKILL.md"
        assert skill_file.exists(), f"SKILL.md does not exist in plugin-development"
        assert skill_file.is_file(), f"SKILL.md is not a file"

    def test_plugin_development_has_frontmatter(self, skills_dir):
        """Test that plugin-development/SKILL.md has YAML frontmatter."""
        skill_file = skills_dir / "plugin-development" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Skill should start with frontmatter delimiter ---"
        assert "---" in content[3:], "Skill should have closing frontmatter delimiter ---"

    def test_plugin_development_frontmatter_valid(self, skills_dir):
        """Test that plugin-development/SKILL.md has valid YAML frontmatter."""
        skill_file = skills_dir / "plugin-development" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        assert len(parts) >= 3, "Frontmatter should be properly delimited"

        frontmatter_str = parts[1].strip()
        frontmatter = yaml.safe_load(frontmatter_str)

        assert frontmatter is not None, "Frontmatter should be valid YAML"
        assert "name" in frontmatter, "Frontmatter must include 'name'"
        assert "description" in frontmatter, "Frontmatter must include 'description'"

    def test_plugin_development_name_matches(self, skills_dir):
        """Test that plugin-development skill name matches directory name."""
        skill_file = skills_dir / "plugin-development" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        skill_name = frontmatter.get("name", "")

        assert skill_name == "plugin-development", \
            f"Skill name should be 'plugin-development', got '{skill_name}'"

    def test_plugin_development_description_length(self, skills_dir):
        """Test that plugin-development description is within 1024 character limit."""
        skill_file = skills_dir / "plugin-development" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "")

        assert len(description) <= 1024, \
            f"Description must be max 1024 characters, got {len(description)}"

    def test_plugin_development_has_trigger_keywords(self, skills_dir):
        """Test that plugin-development description includes activation triggers."""
        skill_file = skills_dir / "plugin-development" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "").lower()

        # Should mention plugin creation, development, structure
        trigger_keywords = ["plugin", "create", "develop", "structure", "component"]
        has_trigger = any(keyword in description for keyword in trigger_keywords)
        assert has_trigger, "Description should include plugin development trigger keywords"

    def test_plugin_development_has_supporting_docs(self, skills_dir):
        """Test that plugin-development skill has supporting documentation."""
        skill_dir = skills_dir / "plugin-development"
        spec_ref = skill_dir / "spec-reference.md"

        assert spec_ref.exists(), \
            "plugin-development should include spec-reference.md supporting doc"


class TestPluginValidationSkill:
    """Test suite for plugin-validation skill."""

    def test_plugin_validation_skill_dir_exists(self, skills_dir):
        """Test that plugin-validation skill directory exists."""
        skill_dir = skills_dir / "plugin-validation"
        assert skill_dir.exists(), f"plugin-validation directory does not exist"
        assert skill_dir.is_dir(), f"plugin-validation is not a directory"

    def test_plugin_validation_skill_file_exists(self, skills_dir):
        """Test that plugin-validation/SKILL.md file exists."""
        skill_file = skills_dir / "plugin-validation" / "SKILL.md"
        assert skill_file.exists(), f"SKILL.md does not exist in plugin-validation"
        assert skill_file.is_file(), f"SKILL.md is not a file"

    def test_plugin_validation_has_frontmatter(self, skills_dir):
        """Test that plugin-validation/SKILL.md has YAML frontmatter."""
        skill_file = skills_dir / "plugin-validation" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Skill should start with frontmatter"
        assert "---" in content[3:], "Skill should have closing frontmatter"

    def test_plugin_validation_frontmatter_valid(self, skills_dir):
        """Test that plugin-validation/SKILL.md has valid YAML frontmatter."""
        skill_file = skills_dir / "plugin-validation" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        assert len(parts) >= 3, "Frontmatter should be properly delimited"

        frontmatter_str = parts[1].strip()
        frontmatter = yaml.safe_load(frontmatter_str)

        assert frontmatter is not None, "Frontmatter should be valid YAML"
        assert "name" in frontmatter, "Frontmatter must include 'name'"
        assert "description" in frontmatter, "Frontmatter must include 'description'"

    def test_plugin_validation_name_matches(self, skills_dir):
        """Test that plugin-validation skill name matches directory name."""
        skill_file = skills_dir / "plugin-validation" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        skill_name = frontmatter.get("name", "")

        assert skill_name == "plugin-validation", \
            f"Skill name should be 'plugin-validation', got '{skill_name}'"

    def test_plugin_validation_description_length(self, skills_dir):
        """Test that plugin-validation description is within 1024 character limit."""
        skill_file = skills_dir / "plugin-validation" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "")

        assert len(description) <= 1024, \
            f"Description must be max 1024 characters, got {len(description)}"

    def test_plugin_validation_has_trigger_keywords(self, skills_dir):
        """Test that plugin-validation description includes validation triggers."""
        skill_file = skills_dir / "plugin-validation" / "SKILL.md"
        with open(skill_file, 'r') as f:
            content = f.read()

        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1].strip())
        description = frontmatter.get("description", "").lower()

        # Should mention validation, errors, checking
        trigger_keywords = ["validat", "check", "error", "specification", "compliance"]
        has_trigger = any(keyword in description for keyword in trigger_keywords)
        assert has_trigger, "Description should include validation trigger keywords"

    def test_plugin_validation_has_supporting_docs(self, skills_dir):
        """Test that plugin-validation skill has supporting documentation."""
        skill_dir = skills_dir / "plugin-validation"
        common_errors = skill_dir / "common-errors.md"

        assert common_errors.exists(), \
            "plugin-validation should include common-errors.md supporting doc"


class TestSkillFrontmatterFormat:
    """Test frontmatter format compliance across all skills."""

    def test_all_skills_have_name_and_description(self, skills_dir):
        """Test that all skills have name and description in frontmatter."""
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        assert len(skill_dirs) >= 2, "Should have at least 2 skill directories"

        for skill_dir in skill_dirs:
            skill_file = skill_dir / "SKILL.md"
            assert skill_file.exists(), \
                f"{skill_dir.name}/SKILL.md should exist"

            with open(skill_file, 'r') as f:
                content = f.read()

            parts = content.split("---", 2)
            assert len(parts) >= 3, f"{skill_dir.name}/SKILL.md should have frontmatter"

            frontmatter = yaml.safe_load(parts[1].strip())
            assert "name" in frontmatter, \
                f"{skill_dir.name}/SKILL.md must have 'name' in frontmatter"
            assert "description" in frontmatter, \
                f"{skill_dir.name}/SKILL.md must have 'description' in frontmatter"

    def test_all_skills_frontmatter_properly_closed(self, skills_dir):
        """Test that all skills have properly closed frontmatter."""
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]

        for skill_dir in skill_dirs:
            skill_file = skill_dir / "SKILL.md"
            with open(skill_file, 'r') as f:
                content = f.read()

            assert content.startswith("---"), \
                f"{skill_dir.name}/SKILL.md should start with ---"

            assert content.count("---") >= 2, \
                f"{skill_dir.name}/SKILL.md should have closing ---"

    def test_all_skills_have_content_after_frontmatter(self, skills_dir):
        """Test that all skills have content after frontmatter."""
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]

        for skill_dir in skill_dirs:
            skill_file = skill_dir / "SKILL.md"
            with open(skill_file, 'r') as f:
                content = f.read()

            parts = content.split("---", 2)
            body = parts[2].strip()
            assert len(body) > 0, \
                f"{skill_dir.name}/SKILL.md should have content after frontmatter"
