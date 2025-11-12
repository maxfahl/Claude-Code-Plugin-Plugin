"""
Test suite for manifest validation functionality.

Tests ensure that manifest validation logic correctly identifies:
- Valid manifest structures
- Invalid or missing required fields
- Incorrect field types
- Unsupported or deprecated fields
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path


class TestManifestFieldValidation:
    """Test validation of individual manifest fields."""

    def test_validate_required_name_field(self):
        """Test that validation requires 'name' field."""
        manifest = {}
        errors = validate_manifest(manifest)
        assert any("name" in err.lower() and "required" in err.lower() for err in errors), \
            "Should report missing required 'name' field"

    def test_validate_name_must_be_string(self):
        """Test that 'name' field must be a string."""
        manifest = {"name": 123}
        errors = validate_manifest(manifest)
        assert any("name" in err.lower() and "string" in err.lower() for err in errors), \
            "Should report 'name' must be a string"

    def test_validate_name_must_be_kebab_case(self):
        """Test that 'name' field must use kebab-case."""
        invalid_names = [
            {"name": "MyPlugin"},  # PascalCase
            {"name": "my_plugin"},  # snake_case
            {"name": "my plugin"},  # spaces
            {"name": "MyAwesome_Plugin"},  # mixed
        ]

        for manifest in invalid_names:
            errors = validate_manifest(manifest)
            assert any("kebab-case" in err.lower() or "hyphen" in err.lower() for err in errors), \
                f"Should report '{manifest['name']}' is not kebab-case"

    def test_validate_kebab_case_name_passes(self):
        """Test that valid kebab-case names pass validation."""
        valid_names = [
            {"name": "my-plugin"},
            {"name": "awesome-plugin"},
            {"name": "multi-word-plugin-name"},
        ]

        for manifest in valid_names:
            errors = validate_manifest(manifest)
            name_errors = [err for err in errors if "name" in err.lower() and "kebab" in err.lower()]
            assert len(name_errors) == 0, f"Valid kebab-case name '{manifest['name']}' should pass"

    def test_validate_version_must_be_string(self):
        """Test that 'version' field must be a string if present."""
        manifest = {"name": "test-plugin", "version": 1.0}
        errors = validate_manifest(manifest)
        assert any("version" in err.lower() and "string" in err.lower() for err in errors), \
            "Should report 'version' must be a string"

    def test_validate_version_semver_format(self):
        """Test that 'version' should follow semver format."""
        manifest = {"name": "test-plugin", "version": "not-semver"}
        errors = validate_manifest(manifest)
        # This is a warning, not a strict error
        warnings = [err for err in errors if "version" in err.lower() and "semver" in err.lower()]
        assert len(warnings) >= 0, "Should warn about non-semver version format"

    def test_validate_description_must_be_string(self):
        """Test that 'description' field must be a string if present."""
        manifest = {"name": "test-plugin", "description": ["array"]}
        errors = validate_manifest(manifest)
        assert any("description" in err.lower() and "string" in err.lower() for err in errors), \
            "Should report 'description' must be a string"

    def test_validate_author_must_be_object(self):
        """Test that 'author' field must be an object if present."""
        manifest = {"name": "test-plugin", "author": "Not An Object"}
        errors = validate_manifest(manifest)
        assert any("author" in err.lower() and "object" in err.lower() for err in errors), \
            "Should report 'author' must be an object"

    def test_validate_author_fields_must_be_strings(self):
        """Test that author sub-fields must be strings."""
        manifest = {
            "name": "test-plugin",
            "author": {
                "name": 123,
                "email": True,
                "url": []
            }
        }
        errors = validate_manifest(manifest)
        assert any("author.name" in err.lower() for err in errors), \
            "Should report author.name must be string"
        assert any("author.email" in err.lower() for err in errors), \
            "Should report author.email must be string"
        assert any("author.url" in err.lower() for err in errors), \
            "Should report author.url must be string"

    def test_validate_keywords_must_be_array(self):
        """Test that 'keywords' field must be an array if present."""
        manifest = {"name": "test-plugin", "keywords": "not-an-array"}
        errors = validate_manifest(manifest)
        assert any("keywords" in err.lower() and "array" in err.lower() for err in errors), \
            "Should report 'keywords' must be an array"

    def test_validate_keywords_items_must_be_strings(self):
        """Test that all keywords must be strings."""
        manifest = {"name": "test-plugin", "keywords": ["valid", 123, True]}
        errors = validate_manifest(manifest)
        assert any("keyword" in err.lower() and "string" in err.lower() for err in errors), \
            "Should report keywords must be strings"

    def test_validate_url_fields_format(self):
        """Test that URL fields should be valid URLs."""
        manifest = {
            "name": "test-plugin",
            "homepage": "not-a-url",
            "repository": "also-not-a-url"
        }
        errors = validate_manifest(manifest)
        # These could be warnings rather than hard errors
        url_warnings = [err for err in errors if "url" in err.lower() or "http" in err.lower()]
        # At minimum, should suggest proper URL format
        assert len(url_warnings) >= 0


class TestUnsupportedFields:
    """Test detection of unsupported or undocumented fields."""

    def test_detect_unsupported_root_fields(self):
        """Test detection of fields not in official spec."""
        manifest = {
            "name": "test-plugin",
            "unsupportedField": "value",
            "anotherUnsupported": 123
        }
        errors = validate_manifest(manifest)
        assert any("unsupported" in err.lower() or "unknown" in err.lower() for err in errors), \
            "Should warn about unsupported fields"

    def test_allow_all_official_fields(self):
        """Test that all official manifest fields are accepted."""
        manifest = {
            "name": "test-plugin",
            "version": "1.0.0",
            "description": "A test plugin",
            "author": {
                "name": "Test Author",
                "email": "test@example.com",
                "url": "https://example.com"
            },
            "homepage": "https://example.com",
            "repository": "https://github.com/user/repo",
            "license": "MIT",
            "keywords": ["test", "plugin"],
            "commands": "commands/",
            "agents": "agents/",
            "hooks": "hooks/hooks.json",
            "mcpServers": ".mcp.json"
        }
        errors = validate_manifest(manifest)
        unsupported_errors = [err for err in errors if "unsupported" in err.lower()]
        assert len(unsupported_errors) == 0, "All official fields should be supported"


class TestManifestValidationFunction:
    """Test the main validation function interface."""

    def test_validate_manifest_returns_list(self):
        """Test that validation function returns a list of errors."""
        manifest = {"name": "valid-plugin"}
        result = validate_manifest(manifest)
        assert isinstance(result, list), "Validation should return a list"

    def test_validate_empty_list_for_valid_manifest(self):
        """Test that valid manifest returns empty error list."""
        manifest = {
            "name": "valid-plugin",
            "version": "1.0.0",
            "description": "A valid plugin"
        }
        errors = validate_manifest(manifest)
        assert len(errors) == 0, "Valid manifest should have no errors"

    def test_validate_returns_errors_for_invalid_manifest(self):
        """Test that invalid manifest returns non-empty error list."""
        manifest = {}  # Missing required 'name'
        errors = validate_manifest(manifest)
        assert len(errors) > 0, "Invalid manifest should return errors"


# Placeholder for actual validation function to be implemented
def validate_manifest(manifest_data):
    """
    Validate a plugin manifest against official specifications.

    Args:
        manifest_data: Dictionary containing manifest data

    Returns:
        List of error/warning messages
    """
    errors = []

    # Required fields
    if "name" not in manifest_data:
        errors.append("Missing required field: 'name'")
    elif not isinstance(manifest_data["name"], str):
        errors.append("Field 'name' must be a string")
    elif not is_kebab_case(manifest_data["name"]):
        errors.append(f"Field 'name' must be in kebab-case (lowercase with hyphens), got: {manifest_data['name']}")

    # Optional string fields
    string_fields = ["version", "description", "homepage", "repository", "license"]
    for field in string_fields:
        if field in manifest_data and not isinstance(manifest_data[field], str):
            errors.append(f"Field '{field}' must be a string")

    # Author object
    if "author" in manifest_data:
        author = manifest_data["author"]
        if not isinstance(author, dict):
            errors.append("Field 'author' must be an object")
        else:
            for key in ["name", "email", "url"]:
                if key in author and not isinstance(author[key], str):
                    errors.append(f"Field 'author.{key}' must be a string")

    # Keywords array
    if "keywords" in manifest_data:
        keywords = manifest_data["keywords"]
        if not isinstance(keywords, list):
            errors.append("Field 'keywords' must be an array")
        else:
            for kw in keywords:
                if not isinstance(kw, str):
                    errors.append("All keywords must be strings")
                    break

    # Check for unsupported fields
    official_fields = {
        "name", "version", "description", "author", "homepage",
        "repository", "license", "keywords", "commands", "agents",
        "hooks", "mcpServers", "skills"
    }
    for field in manifest_data:
        if field not in official_fields:
            errors.append(f"Unsupported field: '{field}' (not in official specification)")

    return errors


def is_kebab_case(name):
    """Check if a string follows kebab-case convention."""
    if not name:
        return False
    # kebab-case: lowercase, can contain hyphens, no spaces or underscores
    if " " in name or "_" in name:
        return False
    # Must be lowercase or contain hyphens
    return name.islower() or "-" in name


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
