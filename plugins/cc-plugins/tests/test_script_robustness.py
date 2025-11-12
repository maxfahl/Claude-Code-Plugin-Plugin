#!/usr/bin/env python3
"""
Test suite for script robustness and error handling.

Tests that all scripts handle:
- Invalid inputs (non-existent paths, malformed data)
- Edge cases (empty directories, special characters)
- Missing dependencies
- Permission errors
- Input validation
- Helpful usage messages
- Cross-platform compatibility
"""

import json
import tempfile
import shutil
import pytest
from pathlib import Path
import subprocess
import os
import sys


class TestScaffoldInputValidation:
    """Test that scaffold script validates input."""

    def test_scaffold_rejects_empty_name(self):
        """Test scaffold rejects empty plugin name."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--name", ""],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode != 0

    def test_scaffold_rejects_invalid_characters(self):
        """Test scaffold rejects names with invalid characters."""
        invalid_names = ["MyPlugin", "my_plugin", "my@plugin", "my.plugin"]
        for name in invalid_names:
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py", "--name", name],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode != 0, f"Should reject {name}"

    def test_scaffold_accepts_valid_kebab_case(self):
        """Test scaffold accepts valid kebab-case names."""
        valid_names = ["test-plugin", "my-awesome-plugin", "a", "my-123"]
        for name in valid_names:
            with tempfile.TemporaryDirectory() as tmpdir:
                result = subprocess.run(
                    ["python", "scripts/scaffold-plugin.py", 
                     "--name", name, "--output", tmpdir],
                    capture_output=True,
                    text=True,
                    cwd=Path(__file__).parent.parent
                )
                assert result.returncode == 0, f"Should accept {name}"


class TestScaffoldEdgeCases:
    """Test handling of edge cases."""

    def test_scaffold_with_unicode_description(self):
        """Test scaffold handles unicode in description."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py",
                 "--name", "test-plugin",
                 "--description", "Plugin with émojis 🎉",
                 "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode == 0

    def test_scaffold_with_special_author_name(self):
        """Test scaffold handles special characters in author."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py",
                 "--name", "test-plugin",
                 "--author", "François Müller-O'Brien",
                 "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode == 0
            # Verify manifest preserves author name
            manifest_path = Path(tmpdir) / "test-plugin" / ".claude-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text())
            assert "François" in manifest["author"]["name"]

    def test_scaffold_existing_directory_error(self):
        """Test scaffold handles attempt to create in existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir) / "test-plugin"
            plugin_dir.mkdir()
            (plugin_dir / "existing.txt").write_text("content")

            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py",
                 "--name", "test-plugin",
                 "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode != 0

    def test_validator_with_empty_directory(self):
        """Test validator handles empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            # Should fail validation
            assert result.returncode != 0

    def test_validator_with_malformed_json(self):
        """Test validator handles malformed JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir) / "test-plugin"
            plugin_dir.mkdir()
            (plugin_dir / ".claude-plugin").mkdir()
            (plugin_dir / ".claude-plugin" / "plugin.json").write_text("{invalid json")

            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", str(plugin_dir)],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode != 0


class TestErrorHandling:
    """Test error handling in scripts."""

    def test_scaffold_handles_permission_errors(self):
        """Test scaffold handles permission errors gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a read-only directory
            readonly_dir = Path(tmpdir) / "readonly"
            readonly_dir.mkdir()
            readonly_dir.chmod(0o444)

            try:
                result = subprocess.run(
                    ["python", "scripts/scaffold-plugin.py",
                     "--name", "test", "--output", str(readonly_dir)],
                    capture_output=True,
                    text=True,
                    cwd=Path(__file__).parent.parent
                )
                # Should fail gracefully
                assert result.returncode != 0
            finally:
                readonly_dir.chmod(0o755)

    def test_validator_handles_nonexistent_path(self):
        """Test validator handles non-existent path."""
        result = subprocess.run(
            ["python", "scripts/validate-plugin.py", "/nonexistent/path"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        # Should fail gracefully
        assert result.returncode != 0

    def test_validator_handles_file_not_directory(self):
        """Test validator handles file path instead of directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "plugin.txt"
            file_path.write_text("not a directory")

            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", str(file_path)],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            # Should fail
            assert result.returncode != 0


class TestDataIntegrity:
    """Test that scripts maintain data integrity."""

    def test_scaffold_preserves_manifest_data(self):
        """Test scaffold preserves all manifest data correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py",
                 "--name", "test-plugin",
                 "--author", "Test Author",
                 "--description", "Test Description",
                 "--version", "2.0.0",
                 "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode == 0

            # Verify manifest
            manifest_path = Path(tmpdir) / "test-plugin" / ".claude-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text())

            assert manifest["name"] == "test-plugin"
            assert manifest["author"]["name"] == "Test Author"
            assert manifest["description"] == "Test Description"
            assert manifest["version"] == "2.0.0"

    def test_scaffold_preserves_unicode_data(self):
        """Test scaffold preserves unicode in manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py",
                 "--name", "test-plugin",
                 "--description", "Plugin with unicode: café, 日本語",
                 "--author", "François Müller",
                 "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode == 0

            manifest = json.loads(
                (Path(tmpdir) / "test-plugin" / ".claude-plugin" / "plugin.json").read_text()
            )
            assert "café" in manifest["description"]
            assert "François" in manifest["author"]["name"]


class TestScriptExecution:
    """Test that scripts execute without errors."""

    def test_scaffold_main_returns_success_code(self):
        """Test scaffold main function returns proper exit code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py",
                 "--name", "test-plugin", "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            assert result.returncode == 0

    def test_scaffold_main_handles_error_exit_code(self):
        """Test scaffold main returns error code on failure."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--name", "InvalidName"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode != 0

    def test_validate_main_returns_error_code_invalid(self):
        """Test validate main returns error code for invalid plugin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            # Empty directory should be invalid
            assert result.returncode != 0


class TestCrossPlatformCompatibility:
    """Test cross-platform compatibility."""

    def test_scripts_use_pathlib(self):
        """Test that scripts use pathlib for cross-platform paths."""
        scaffold_path = Path(__file__).parent.parent / "scripts" / "scaffold-plugin.py"
        content = scaffold_path.read_text()
        # Should use Path class
        assert "Path" in content
        assert "pathlib" in content.lower()

    def test_scripts_use_standard_library(self):
        """Test that file operations use standard library."""
        validator_path = Path(__file__).parent.parent / "scripts" / "validate-plugin.py"
        content = validator_path.read_text()
        # Should use standard library for JSON
        assert "import json" in content
        # Validators module should import yaml
        validators_path = Path(__file__).parent.parent / "scripts" / "validators.py"
        validators_content = validators_path.read_text()
        assert "import yaml" in validators_content


class TestHelpMessages:
    """Test that scripts provide helpful messages."""

    def test_scaffold_help_text_is_useful(self):
        """Test that scaffold help text is helpful."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        # Should provide help
        assert "name" in result.stdout.lower()
        assert result.returncode == 0 or "help" in result.stdout.lower()

    def test_error_messages_are_readable(self):
        """Test that error messages are readable."""
        result = subprocess.run(
            ["python", "scripts/scaffold-plugin.py", "--name", "Invalid_Name"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        output = result.stderr + result.stdout
        # Should have readable error message
        assert len(output) > 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
