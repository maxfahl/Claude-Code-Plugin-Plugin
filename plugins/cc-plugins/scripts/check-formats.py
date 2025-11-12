#!/usr/bin/env python3
"""
Format checker script for Claude Code plugins.

Validates:
- YAML frontmatter syntax in .md files
- JSON file syntax (plugin.json, hooks.json, .mcp.json)
- Markdown formatting issues
- Reports format errors with line numbers

Usage:
    ./scripts/check-formats.py [--json-only] [--md-only] [path]

Exit codes:
    0: All formats valid
    1: Format errors found
    2: Script execution error

Reference: https://code.claude.com/docs/en/plugin-development
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


class FormatChecker:
    """Checks formatting of plugin files."""

    def __init__(self, root_path: Path, check_json: bool = True, check_md: bool = True):
        """Initialize format checker."""
        self.root_path = root_path
        self.check_json = check_json
        self.check_md = check_md
        self.errors: List[Dict] = []

    def check_all(self) -> bool:
        """
        Check all plugin files for format issues.

        Returns:
            True if no errors found, False otherwise
        """
        if not self.root_path.exists():
            self.errors.append({
                'file': str(self.root_path),
                'line': 0,
                'error': f"Path does not exist: {self.root_path}"
            })
            return False

        # Check markdown files with frontmatter
        if self.check_md:
            self._check_markdown_files()

        # Check JSON files
        if self.check_json:
            self._check_json_files()

        return len(self.errors) == 0

    def _check_markdown_files(self):
        """Check all markdown files in the plugin."""
        # Check commands
        commands_dir = self.root_path / "commands"
        if commands_dir.exists():
            for md_file in commands_dir.glob("*.md"):
                self._check_markdown_file(md_file)

        # Check agents
        agents_dir = self.root_path / "agents"
        if agents_dir.exists():
            for md_file in agents_dir.glob("*.md"):
                self._check_markdown_file(md_file)

        # Check skills
        skills_dir = self.root_path / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        self._check_markdown_file(skill_md)

    def _check_markdown_file(self, file_path: Path):
        """Check a single markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append({
                'file': str(file_path),
                'line': 0,
                'error': f"Error reading file: {e}"
            })
            return

        lines = content.split('\n')

        # Check for frontmatter
        if lines and lines[0].strip() == '---':
            # Find closing delimiter
            end_idx = None
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_idx = i
                    break

            if end_idx is None:
                self.errors.append({
                    'file': str(file_path),
                    'line': 1,
                    'error': 'Missing closing --- delimiter for frontmatter'
                })
                return

            # Check YAML syntax
            frontmatter_str = '\n'.join(lines[1:end_idx])
            try:
                yaml.safe_load(frontmatter_str)
            except yaml.YAMLError as e:
                # Extract line number from error if possible
                error_line = 1
                if hasattr(e, 'problem_mark'):
                    error_line = 1 + e.problem_mark.line
                self.errors.append({
                    'file': str(file_path),
                    'line': error_line,
                    'error': f"Invalid YAML in frontmatter: {str(e).split(chr(10))[0]}"
                })
                return

        # Check markdown formatting
        self._check_markdown_format(file_path, lines)

    def _check_markdown_format(self, file_path: Path, lines: List[str]):
        """Check markdown formatting issues."""
        # Check for missing final newline
        if lines and lines[-1] != '':
            # Only warn if there's actual content
            content = file_path.read_text(encoding='utf-8')
            if content and not content.endswith('\n'):
                self.errors.append({
                    'file': str(file_path),
                    'line': len(lines),
                    'error': 'Missing final newline at end of file'
                })

        # Check for trailing spaces
        for i, line in enumerate(lines, 1):
            if line and line != line.rstrip():
                self.errors.append({
                    'file': str(file_path),
                    'line': i,
                    'error': 'Line contains trailing whitespace'
                })

    def _check_json_files(self):
        """Check JSON files for validity."""
        json_files = [
            self.root_path / ".claude-plugin" / "plugin.json",
            self.root_path / ".mcp.json",
            self.root_path / "hooks" / "hooks.json",
        ]

        for json_file in json_files:
            if json_file.exists():
                self._check_json_file(json_file)

    def _check_json_file(self, file_path: Path):
        """Check a single JSON file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append({
                'file': str(file_path),
                'line': 0,
                'error': f"Error reading file: {e}"
            })
            return

        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            self.errors.append({
                'file': str(file_path),
                'line': e.lineno,
                'error': f"Invalid JSON: {e.msg} (column {e.colno})"
            })
            return

    def print_report(self, as_json: bool = False):
        """Print format check report."""
        if as_json:
            print(json.dumps(self.errors, indent=2))
            return

        if not self.errors:
            print("✓ All files have valid format")
            return

        print(f"\nFORMAT ERRORS ({len(self.errors)}):\n")
        for error in self.errors:
            file_path = error['file']
            line_num = error['line']
            msg = error['error']

            print(f"{file_path}:{line_num}")
            print(f"  {msg}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check format validity of plugin files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./scripts/check-formats.py                 Check all formats in current directory
  ./scripts/check-formats.py /path/to/plugin  Check specific plugin
  ./scripts/check-formats.py --json-only .   Check only JSON files
  ./scripts/check-formats.py --md-only .     Check only markdown files
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to plugin directory (default: current directory)'
    )

    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Check only JSON files'
    )

    parser.add_argument(
        '--md-only',
        action='store_true',
        help='Check only markdown files'
    )

    parser.add_argument(
        '--json-output',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    plugin_root = Path(args.path).resolve()

    # Determine what to check
    check_json = not args.md_only
    check_md = not args.json_only

    checker = FormatChecker(plugin_root, check_json=check_json, check_md=check_md)

    try:
        is_valid = checker.check_all()
    except Exception as e:
        print(f"Fatal error during format check: {e}", file=sys.stderr)
        return 2

    checker.print_report(as_json=args.json_output)

    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
