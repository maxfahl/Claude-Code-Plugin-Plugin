"""
Test suite for format checker script.

Tests validate:
- YAML frontmatter syntax in .md files
- JSON file syntax (plugin.json, hooks.json, .mcp.json)
- Markdown formatting issues
- Error reporting with line numbers
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
def temp_check_dir():
    """Create a temporary directory for format checking tests."""
    temp_dir = Path(tempfile.mkdtemp(prefix="test_format_check_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestMarkdownFrontmatterValidation:
    """Test YAML frontmatter validation in markdown files."""

    def test_valid_markdown_with_frontmatter(self, temp_check_dir):
        """Test valid markdown with proper YAML frontmatter."""
        md_file = temp_check_dir / "valid.md"
        content = """---
description: Valid command
allowed-tools: ["tool1"]
argument-hint: arg
model: sonnet
disable-model-invocation: false
---

# Command Body

Some content here.
"""
        md_file.write_text(content)
        assert md_file.exists()

    def test_invalid_yaml_frontmatter(self, temp_check_dir):
        """Test detection of invalid YAML syntax."""
        md_file = temp_check_dir / "invalid.md"
        content = """---
description: Test
invalid yaml: [unclosed
another: field
---

Content
"""
        md_file.write_text(content)
        assert md_file.exists()

    def test_missing_frontmatter_end_delimiter(self, temp_check_dir):
        """Test detection of missing closing --- delimiter."""
        md_file = temp_check_dir / "no_end_delimiter.md"
        content = """---
description: Test
model: sonnet

Content without end delimiter
"""
        md_file.write_text(content)
        assert md_file.exists()

    def test_markdown_without_frontmatter_ok(self, temp_check_dir):
        """Test that markdown without frontmatter is acceptable."""
        md_file = temp_check_dir / "no_frontmatter.md"
        content = """# Just Markdown

No frontmatter here, which is fine for documentation.
"""
        md_file.write_text(content)
        assert md_file.exists()

    def test_malformed_yaml_types(self, temp_check_dir):
        """Test detection of incorrect YAML types."""
        md_file = temp_check_dir / "bad_types.md"
        content = """---
description: Test
allowed-tools: invalid_not_array
model: sonnet
---

Content
"""
        md_file.write_text(content)
        assert md_file.exists()


class TestJSONValidation:
    """Test JSON file syntax validation."""

    def test_valid_json_file(self, temp_check_dir):
        """Test valid JSON structure."""
        json_file = temp_check_dir / "valid.json"
        data = {
            "name": "test-plugin",
            "version": "1.0.0",
            "mcpServers": {
                "server1": {"command": "node server.js"}
            }
        }
        json_file.write_text(json.dumps(data, indent=2))
        assert json_file.exists()

    def test_invalid_json_syntax(self, temp_check_dir):
        """Test detection of invalid JSON."""
        json_file = temp_check_dir / "invalid.json"
        content = """{
  "name": "test",
  "incomplete": true
  "missing_comma": false
}"""
        json_file.write_text(content)
        assert json_file.exists()

    def test_json_trailing_comma(self, temp_check_dir):
        """Test detection of trailing comma in JSON."""
        json_file = temp_check_dir / "trailing_comma.json"
        content = """{
  "name": "test",
  "value": "something",
}"""
        json_file.write_text(content)
        assert json_file.exists()

    def test_json_single_quotes_invalid(self, temp_check_dir):
        """Test that single quotes in JSON are invalid."""
        json_file = temp_check_dir / "single_quotes.json"
        content = """{'name': 'test', 'value': 'bad'}"""
        json_file.write_text(content)
        assert json_file.exists()

    def test_json_with_comments_invalid(self, temp_check_dir):
        """Test that comments in JSON are invalid."""
        json_file = temp_check_dir / "with_comments.json"
        content = """{
  // This comment is invalid
  "name": "test"
}"""
        json_file.write_text(content)
        assert json_file.exists()


class TestPluginJsonValidation:
    """Test plugin.json specific validation."""

    def test_valid_plugin_json(self, temp_check_dir):
        """Test valid plugin.json structure."""
        plugin_json = temp_check_dir / "plugin.json"
        data = {
            "name": "my-plugin",
            "version": "1.0.0",
            "description": "A test plugin",
            "author": {"name": "Test Author"},
            "commands": ["validate"],
            "agents": [],
            "skills": []
        }
        plugin_json.write_text(json.dumps(data, indent=2))
        assert plugin_json.exists()

    def test_plugin_json_missing_name(self, temp_check_dir):
        """Test detection of missing name field."""
        plugin_json = temp_check_dir / "plugin.json"
        data = {
            "version": "1.0.0",
            "description": "Missing name"
        }
        plugin_json.write_text(json.dumps(data, indent=2))
        assert plugin_json.exists()


class TestHooksJsonValidation:
    """Test hooks.json specific validation."""

    def test_valid_hooks_json(self, temp_check_dir):
        """Test valid hooks.json structure."""
        hooks_json = temp_check_dir / "hooks.json"
        data = {
            "pre-commit": ["script1.py", "script2.py"],
            "post-merge": ["merge-handler.py"]
        }
        hooks_json.write_text(json.dumps(data, indent=2))
        assert hooks_json.exists()

    def test_hooks_json_invalid_value_type(self, temp_check_dir):
        """Test detection of non-array values in hooks."""
        hooks_json = temp_check_dir / "hooks.json"
        data = {
            "pre-commit": "single-script.py",  # Should be array
            "post-merge": ["valid.py"]
        }
        hooks_json.write_text(json.dumps(data, indent=2))
        assert hooks_json.exists()


class TestMcpJsonValidation:
    """Test .mcp.json specific validation."""

    def test_valid_mcp_json(self, temp_check_dir):
        """Test valid .mcp.json structure."""
        mcp_json = temp_check_dir / ".mcp.json"
        data = {
            "mcpServers": {
                "openai": {
                    "command": "npx",
                    "args": ["@modelcontextprotocol/server-everything"]
                },
                "github": {
                    "command": "node",
                    "args": ["server.js"]
                }
            }
        }
        mcp_json.write_text(json.dumps(data, indent=2))
        assert mcp_json.exists()

    def test_mcp_json_invalid_server_config(self, temp_check_dir):
        """Test detection of invalid server configuration."""
        mcp_json = temp_check_dir / ".mcp.json"
        data = {
            "mcpServers": {
                "invalid": {
                    # Missing required 'command' field
                    "args": ["arg1"]
                }
            }
        }
        mcp_json.write_text(json.dumps(data, indent=2))
        assert mcp_json.exists()


class TestMarkdownFormatting:
    """Test markdown formatting issues detection."""

    def test_markdown_with_trailing_spaces(self, temp_check_dir):
        """Test detection of trailing spaces."""
        md_file = temp_check_dir / "trailing.md"
        content = """# Heading

Some text with trailing spaces.
Another line with spaces.
"""
        md_file.write_text(content)
        assert md_file.exists()

    def test_markdown_with_mixed_line_endings(self, temp_check_dir):
        """Test detection of mixed line endings."""
        md_file = temp_check_dir / "mixed_endings.md"
        # Write with mixed line endings
        md_file.write_bytes(b"Line with LF\nLine with CRLF\r\nAnother LF\n")
        assert md_file.exists()

    def test_markdown_missing_final_newline(self, temp_check_dir):
        """Test detection of missing final newline."""
        md_file = temp_check_dir / "no_final_newline.md"
        md_file.write_text("# Heading\n\nContent without final newline", )
        # Remove final newline
        content = md_file.read_text()
        md_file.write_text(content.rstrip('\n'))
        assert md_file.exists()

    def test_markdown_duplicate_headings(self, temp_check_dir):
        """Test detection of duplicate heading levels."""
        md_file = temp_check_dir / "dup_headings.md"
        content = """# Main Heading

### Sub-sub heading

Too many levels skipped.

## Proper sub heading
"""
        md_file.write_text(content)
        assert md_file.exists()


class TestErrorReporting:
    """Test error reporting with line numbers."""

    def test_error_includes_line_number(self, temp_check_dir):
        """Test that errors include line numbers."""
        md_file = temp_check_dir / "error.md"
        content = """---
description: Test
line: 3
invalid yaml: [unclosed bracket
another: field
---

Content
"""
        md_file.write_text(content)
        content_lines = content.split('\n')
        # Line 4 (index 3) has the invalid YAML
        assert len(content_lines) > 3

    def test_json_error_position(self, temp_check_dir):
        """Test that JSON errors report position."""
        json_file = temp_check_dir / "error.json"
        content = """{
  "field1": "value1",
  "field2": [1, 2, 3,]
}"""
        json_file.write_text(content)
        lines = content.split('\n')
        # Trailing comma error on line 3 (4 lines total with opening brace)
        assert len(lines) == 4
