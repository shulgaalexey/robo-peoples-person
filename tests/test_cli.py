"""Tests for CLI functionality."""

from unittest.mock import AsyncMock, patch

import pytest
from click.testing import CliRunner

from src.cli.main import cli


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])

    assert result.exit_code == 0
    assert "Workplace Social Graph AI Agent CLI" in result.output
    assert "person" in result.output
    assert "org" in result.output
    assert "network" in result.output


def test_person_group_help():
    """Test person group help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['person', '--help'])

    assert result.exit_code == 0
    assert "Manage people" in result.output
    assert "add" in result.output
    assert "find-experts" in result.output


def test_network_group_help():
    """Test network group help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['network', '--help'])

    assert result.exit_code == 0
    assert "Network analysis" in result.output
    assert "insights" in result.output
    assert "daily-report" in result.output


def test_setup_group_help():
    """Test setup group help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['setup', '--help'])

    assert result.exit_code == 0
    assert "Setup and initialization" in result.output
    assert "init-db" in result.output
    assert "check-config" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_add_person_command(mock_agent_class):
    """Test add person command."""
    # Mock the agent and its methods
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "✅ Added John Doe successfully"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'person', 'add',
        '--name', 'John Doe',
        '--email', 'john@company.com',
        '--department', 'Engineering',
        '--role', 'Developer'
    ])

    assert result.exit_code == 0
    assert "Added John Doe successfully" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_find_experts_command(mock_agent_class):
    """Test find experts command."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "🔍 Found 3 Python experts"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'person', 'find-experts',
        '--skill', 'Python'
    ])

    assert result.exit_code == 0
    assert "Found 3 Python experts" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_stats_command(mock_agent_class):
    """Test stats command."""
    mock_agent = AsyncMock()
    mock_agent.get_stats.return_value = {
        'total_people': 10,
        'total_relationships': 25,
        'total_departments': 3,
        'network_density': 0.15,
        'largest_department': 'Engineering',
        'departments': {'Engineering': 5, 'Sales': 3, 'HR': 2}
    }
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, ['data', 'stats'])

    assert result.exit_code == 0
    assert "Total people: 10" in result.output
    assert "Total relationships: 25" in result.output
    assert "Engineering: 5" in result.output


@patch('src.cli.main.apply_initial_migration')
def test_init_db_command(mock_migration):
    """Test database initialization command."""
    mock_migration.return_value = None

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'init-db'])

    assert result.exit_code == 0
    assert "Database initialized successfully" in result.output
    mock_migration.assert_called_once()


@patch('src.cli.main.apply_initial_migration')
def test_init_db_command_error(mock_migration):
    """Test database initialization command with error."""
    mock_migration.side_effect = Exception("Connection failed")

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'init-db'])

    assert result.exit_code == 1
    assert "Database initialization failed" in result.output
