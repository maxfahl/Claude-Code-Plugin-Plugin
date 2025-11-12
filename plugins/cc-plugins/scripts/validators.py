#!/usr/bin/env python3
"""
Component validator functions for Claude Code plugins.

This module provides validators for different plugin component types:
- Command files (markdown with YAML frontmatter)
- Agent files (markdown with YAML frontmatter)
- Skill directories (with SKILL.md)
- Hook configurations (hooks.json)
- MCP configurations (.mcp.json)

Reference: https://code.claude.com/docs/en/plugin-development
"""

import json
import yaml
from pathlib import Path
from typing import List, Tuple


def validate_command_file(file_path: Path) -> List[str]:
    """
    Validate a command markdown file.

    Args:
        file_path: Path to the command markdown file

    Returns:
        List of error messages (empty if valid)

    Required frontmatter fields:
        - description: Brief description of the command
        - allowed-tools: Array of tool names the command can use
        - argument-hint: Hint about command arguments
        - model: Model to use (sonnet, opus, haiku)
        - disable-model-invocation: Boolean, whether to disable model invocation
    """
    errors = []

    if not file_path.exists():
        errors.append(f"Command file does not exist: {file_path}")
        return errors

    if not file_path.is_file():
        errors.append(f"Command path is not a file: {file_path}")
        return errors

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Error reading command file {file_path}: {e}")
        return errors

    # Extract frontmatter
    frontmatter, body = _extract_frontmatter(content)

    if frontmatter is None:
        errors.append(f"Command file missing YAML frontmatter: {file_path}")
        errors.append("Expected YAML frontmatter between --- markers at the start of the file")
        return errors

    # Validate required fields
    required_fields = {
        'description': str,
        'allowed-tools': list,
        'argument-hint': str,
        'model': str,
        'disable-model-invocation': bool,
    }

    for field, expected_type in required_fields.items():
        if field not in frontmatter:
            errors.append(
                f"Command file missing required field '{field}' in frontmatter: {file_path}"
            )
        elif expected_type == list:
            if not isinstance(frontmatter[field], list):
                errors.append(
                    f"Field '{field}' must be an array, got {type(frontmatter[field]).__name__}: {file_path}"
                )
            else:
                # Check array contains strings
                for i, item in enumerate(frontmatter[field]):
                    if not isinstance(item, str):
                        errors.append(
                            f"Field '{field}' contains non-string item at index {i}: {file_path}"
                        )
        elif expected_type == bool:
            if not isinstance(frontmatter[field], bool):
                errors.append(
                    f"Field '{field}' must be boolean, got {type(frontmatter[field]).__name__}: {file_path}"
                )
        elif expected_type == str:
            if not isinstance(frontmatter[field], str):
                errors.append(
                    f"Field '{field}' must be string, got {type(frontmatter[field]).__name__}: {file_path}"
                )

    # Validate model value
    if 'model' in frontmatter:
        valid_models = ['sonnet', 'opus', 'haiku']
        if frontmatter['model'] not in valid_models:
            errors.append(
                f"Field 'model' must be one of {valid_models}, got '{frontmatter['model']}': {file_path}"
            )

    return errors


def validate_agent_file(file_path: Path) -> List[str]:
    """
    Validate an agent markdown file.

    Args:
        file_path: Path to the agent markdown file

    Returns:
        List of error messages (empty if valid)

    Required frontmatter fields:
        - description: Brief description of the agent (max 1024 chars)

    Optional frontmatter fields:
        - tools: Array of tool names the agent can use
        - model: Model to use (sonnet, opus, haiku)
    """
    errors = []

    if not file_path.exists():
        errors.append(f"Agent file does not exist: {file_path}")
        return errors

    if not file_path.is_file():
        errors.append(f"Agent path is not a file: {file_path}")
        return errors

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Error reading agent file {file_path}: {e}")
        return errors

    # Extract frontmatter
    frontmatter, body = _extract_frontmatter(content)

    if frontmatter is None:
        errors.append(f"Agent file missing YAML frontmatter: {file_path}")
        errors.append("Expected YAML frontmatter between --- markers at the start of the file")
        return errors

    # Validate required fields
    if 'description' not in frontmatter:
        errors.append(
            f"Agent file missing required field 'description' in frontmatter: {file_path}"
        )
    elif not isinstance(frontmatter['description'], str):
        errors.append(
            f"Field 'description' must be string, got {type(frontmatter['description']).__name__}: {file_path}"
        )
    else:
        if len(frontmatter['description']) > 1024:
            errors.append(
                f"Field 'description' exceeds maximum length of 1024 characters: {file_path}"
            )

    # Validate optional fields
    if 'tools' in frontmatter:
        if not isinstance(frontmatter['tools'], list):
            errors.append(
                f"Field 'tools' must be an array, got {type(frontmatter['tools']).__name__}: {file_path}"
            )
        else:
            for i, item in enumerate(frontmatter['tools']):
                if not isinstance(item, str):
                    errors.append(
                        f"Field 'tools' contains non-string item at index {i}: {file_path}"
                    )

    if 'model' in frontmatter:
        valid_models = ['sonnet', 'opus', 'haiku']
        if frontmatter['model'] not in valid_models:
            errors.append(
                f"Field 'model' must be one of {valid_models}, got '{frontmatter['model']}': {file_path}"
            )

    return errors


def validate_skill_directory(dir_path: Path) -> List[str]:
    """
    Validate a skill directory structure.

    Args:
        dir_path: Path to the skill directory

    Returns:
        List of error messages (empty if valid)

    Validates:
        - Directory exists
        - Contains SKILL.md file
        - SKILL.md has valid YAML frontmatter with required fields
    """
    errors = []

    if not dir_path.exists():
        errors.append(f"Skill directory does not exist: {dir_path}")
        return errors

    if not dir_path.is_dir():
        errors.append(f"Skill path is not a directory: {dir_path}")
        return errors

    skill_md = dir_path / "SKILL.md"

    if not skill_md.exists():
        errors.append(
            f"Skill directory missing required SKILL.md file: {dir_path}"
        )
        return errors

    # Validate SKILL.md content
    skill_errors = _validate_skill_md(skill_md)
    errors.extend(skill_errors)

    return errors


def _validate_skill_md(file_path: Path) -> List[str]:
    """
    Validate SKILL.md file content.

    Args:
        file_path: Path to SKILL.md

    Returns:
        List of error messages
    """
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Error reading SKILL.md: {file_path}: {e}")
        return errors

    # Extract frontmatter
    frontmatter, body = _extract_frontmatter(content)

    if frontmatter is None:
        errors.append(f"SKILL.md missing YAML frontmatter: {file_path}")
        errors.append("Expected YAML frontmatter between --- markers at the start of the file")
        return errors

    # Validate required fields
    if 'name' not in frontmatter:
        errors.append(
            f"SKILL.md missing required field 'name' in frontmatter: {file_path}"
        )
    elif not isinstance(frontmatter['name'], str):
        errors.append(
            f"Field 'name' must be string, got {type(frontmatter['name']).__name__}: {file_path}"
        )
    else:
        # Validate name is kebab-case
        name = frontmatter['name']
        if not _is_kebab_case(name):
            errors.append(
                f"Skill 'name' must be kebab-case (lowercase with hyphens), got '{name}': {file_path}"
            )

    if 'description' not in frontmatter:
        errors.append(
            f"SKILL.md missing required field 'description' in frontmatter: {file_path}"
        )
    elif not isinstance(frontmatter['description'], str):
        errors.append(
            f"Field 'description' must be string, got {type(frontmatter['description']).__name__}: {file_path}"
        )
    else:
        if len(frontmatter['description']) > 1024:
            errors.append(
                f"Field 'description' exceeds maximum length of 1024 characters: {file_path}"
            )

    # Validate optional fields
    if 'allowed-tools' in frontmatter:
        if not isinstance(frontmatter['allowed-tools'], list):
            errors.append(
                f"Field 'allowed-tools' must be an array, got {type(frontmatter['allowed-tools']).__name__}: {file_path}"
            )
        else:
            for i, item in enumerate(frontmatter['allowed-tools']):
                if not isinstance(item, str):
                    errors.append(
                        f"Field 'allowed-tools' contains non-string item at index {i}: {file_path}"
                    )

    if 'tags' in frontmatter:
        if not isinstance(frontmatter['tags'], list):
            errors.append(
                f"Field 'tags' must be an array, got {type(frontmatter['tags']).__name__}: {file_path}"
            )
        else:
            for i, item in enumerate(frontmatter['tags']):
                if not isinstance(item, str):
                    errors.append(
                        f"Field 'tags' contains non-string item at index {i}: {file_path}"
                    )

    return errors


def validate_hooks_config(file_path: Path) -> List[str]:
    """
    Validate hooks.json configuration file.

    Args:
        file_path: Path to hooks.json

    Returns:
        List of error messages (empty if valid)

    Validates:
        - File is valid JSON
        - All hook values are arrays of strings
    """
    errors = []

    if not file_path.exists():
        errors.append(f"Hooks config file does not exist: {file_path}")
        return errors

    if not file_path.is_file():
        errors.append(f"Hooks config path is not a file: {file_path}")
        return errors

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Hooks config contains invalid JSON: {file_path}: {e}")
        return errors
    except Exception as e:
        errors.append(f"Error reading hooks config: {file_path}: {e}")
        return errors

    if not isinstance(config, dict):
        errors.append(f"Hooks config must be a JSON object, got {type(config).__name__}: {file_path}")
        return errors

    # Validate hook values
    for hook_name, scripts in config.items():
        if not isinstance(scripts, list):
            errors.append(
                f"Hook '{hook_name}' value must be an array, got {type(scripts).__name__}: {file_path}"
            )
        else:
            for i, script in enumerate(scripts):
                if not isinstance(script, str):
                    errors.append(
                        f"Hook '{hook_name}' at index {i} must be string, got {type(script).__name__}: {file_path}"
                    )

    return errors


def validate_mcp_config(file_path: Path) -> List[str]:
    """
    Validate .mcp.json configuration file.

    Args:
        file_path: Path to .mcp.json

    Returns:
        List of error messages (empty if valid)

    Validates:
        - File is valid JSON
        - Contains mcpServers object
        - Server configurations are valid
    """
    errors = []

    if not file_path.exists():
        errors.append(f"MCP config file does not exist: {file_path}")
        return errors

    if not file_path.is_file():
        errors.append(f"MCP config path is not a file: {file_path}")
        return errors

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"MCP config contains invalid JSON: {file_path}: {e}")
        return errors
    except Exception as e:
        errors.append(f"Error reading MCP config: {file_path}: {e}")
        return errors

    if not isinstance(config, dict):
        errors.append(f"MCP config must be a JSON object, got {type(config).__name__}: {file_path}")
        return errors

    # Validate mcpServers field if present
    if 'mcpServers' in config:
        if not isinstance(config['mcpServers'], dict):
            errors.append(
                f"Field 'mcpServers' must be an object, got {type(config['mcpServers']).__name__}: {file_path}"
            )
        else:
            # Validate each server configuration
            for server_name, server_config in config['mcpServers'].items():
                if not isinstance(server_config, dict):
                    errors.append(
                        f"Server '{server_name}' configuration must be an object, got {type(server_config).__name__}: {file_path}"
                    )
                else:
                    # Validate required server fields
                    if 'command' not in server_config:
                        errors.append(
                            f"Server '{server_name}' missing required 'command' field: {file_path}"
                        )
                    elif not isinstance(server_config['command'], str):
                        errors.append(
                            f"Server '{server_name}' command must be string, got {type(server_config['command']).__name__}: {file_path}"
                        )

    return errors


def _extract_frontmatter(content: str) -> Tuple[dict | None, str]:
    """
    Extract YAML frontmatter from markdown content.

    Args:
        content: Markdown file content

    Returns:
        Tuple of (frontmatter_dict, body_content) or (None, content) if no frontmatter
    """
    lines = content.split('\n')

    if len(lines) < 3 or lines[0].strip() != '---':
        return None, content

    # Find closing ---
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_index = i
            break

    if end_index is None:
        return None, content

    # Extract frontmatter
    frontmatter_str = '\n'.join(lines[1:end_index])
    body = '\n'.join(lines[end_index + 1:])

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        if frontmatter is None:
            frontmatter = {}
        if not isinstance(frontmatter, dict):
            return None, content
        return frontmatter, body
    except yaml.YAMLError:
        return None, content


def _is_kebab_case(name: str) -> bool:
    """
    Check if a string follows kebab-case convention.

    Args:
        name: String to check

    Returns:
        True if name is in kebab-case (lowercase with hyphens, no spaces/underscores)
    """
    if not name:
        return False

    # Must be lowercase
    if not name.islower():
        return False

    # Can contain hyphens but not spaces or underscores
    if ' ' in name or '_' in name:
        return False

    return True
