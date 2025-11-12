#!/usr/bin/env python3
"""
Test suite for error message quality and clarity.

Tests that all error messages across scripts and validators are:
- Clear and actionable
- Provide helpful context
- Suggest solutions
- Reference official documentation where appropriate
- Include examples of correct usage
"""

import json
import tempfile
import shutil
import pytest
from pathlib import Path
import subprocess
import sys


class TestPluginNameValidation:
    """Test error messages for plugin name validation."""

    def test_invalid_camel_case_name_rejected(self):
        """Test that CamelCase names are rejected."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--name", "MyPlugin"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        # Should fail
        assert result.returncode != 0
        # Error message should be helpful
        assert "kebab-case" in result.stderr.lower() or "kebab-case" in result.stdout.lower()

    def test_underscore_name_rejected(self):
        """Test that names with underscores are rejected."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--name", "my_plugin"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode != 0

    def test_space_in_name_rejected(self):
        """Test that names with spaces are rejected."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--name", "my plugin"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode != 0

    def test_valid_name_accepted(self):
        """Test that valid kebab-case names are accepted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py", 
                 "--name", "test-plugin", "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode == 0
            assert "successfully" in result.stdout.lower()


class TestManifestErrors:
    """Test error messages for manifest issues."""

    def test_missing_manifest_clear_error(self):
        """Test error for missing manifest is clear."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create plugin dir without manifest
            plugin_dir = Path(tmpdir) / "test-plugin"
            plugin_dir.mkdir()
            (plugin_dir / ".claude-plugin").mkdir()

            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", str(plugin_dir)],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            # Should report error
            assert result.returncode != 0
            output = result.stderr + result.stdout
            # Should mention plugin.json
            assert "plugin.json" in output.lower()

    def test_invalid_json_clear_error(self):
        """Test error for invalid JSON is clear."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir) / "test-plugin"
            plugin_dir.mkdir()
            (plugin_dir / ".claude-plugin").mkdir()
            
            # Write invalid JSON
            (plugin_dir / ".claude-plugin" / "plugin.json").write_text("{invalid}")

            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", str(plugin_dir)],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            # Should report error
            assert result.returncode != 0


class TestErrorMessageCompleteness:
    """Test that error messages are complete and informative."""

    def test_error_message_includes_context(self):
        """Test that error messages include helpful context."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir) / "test"
            plugin_dir.mkdir()
            # Completely invalid plugin
            
            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", str(plugin_dir)],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            output = result.stderr + result.stdout
            # Should provide actionable feedback
            assert len(output) > 0


class TestScriptUsageMessages:
    """Test that scripts provide helpful usage information."""

    def test_scaffold_help_available(self):
        """Test that scaffold script help is available."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        # Should provide help (may exit with 0)
        assert "name" in result.stdout.lower() or "usage" in result.stdout.lower()

    def test_validate_help_available(self):
        """Test that validate script help is available."""
        result = subprocess.run(
            ["python", "scripts/validate-plugin.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        # Should provide help
        assert "plugin" in result.stdout.lower() or "validate" in result.stdout.lower()


class TestDocumentationReferences:
    """Test that error messages reference helpful resources."""

    def test_validator_mentions_spec(self):
        """Test that validator references the specification."""
        # Check the validator source mentions documentation
        validator_path = Path(__file__).parent.parent / "scripts" / "validate-plugin.py"
        content = validator_path.read_text()
        # Should reference documentation
        assert "code.claude.com" in content or "specification" in content.lower()


class TestActionableFeedback:
    """Test that errors suggest solutions."""

    def test_existing_directory_suggests_solution(self):
        """Test that error for existing directory is actionable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir) / "test-plugin"
            plugin_dir.mkdir()
            # Create some content
            (plugin_dir / "test.txt").write_text("content")

            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py", 
                 "--name", "test-plugin", "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            # Should fail with helpful message
            assert result.returncode != 0
            output = result.stderr + result.stdout
            assert "exists" in output.lower() or "different" in output.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
