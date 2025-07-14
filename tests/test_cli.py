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


@patch('src.cli.main.initialize_database')
def test_init_db_command(mock_migration):
    """Test database initialization command."""
    mock_migration.return_value = None

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'init-db'])

    assert result.exit_code == 0
    assert "Database initialized successfully" in result.output
    mock_migration.assert_called_once()


@patch('src.cli.main.initialize_database')
def test_init_db_command_error(mock_migration):
    """Test database initialization command with error."""
    mock_migration.side_effect = Exception("Connection failed")

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'init-db'])

    assert result.exit_code == 1
    assert "Database initialization failed" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_who_to_ask_command(mock_agent_class):
    """Test who to ask command."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "🎯 Ask Alice (alice@company.com) - Python expert in Engineering"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'person', 'who-to-ask',
        '--topic', 'Python debugging',
        '--expertise', 'Python'
    ])

    assert result.exit_code == 0
    assert "Ask Alice" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_org_chart_command(mock_agent_class):
    """Test org chart command."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "📊 Engineering Department:\n  - Alice (Lead)\n  - Bob (Developer)"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, ['org', 'chart', '--department', 'Engineering'])

    assert result.exit_code == 0
    assert "Engineering Department" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_org_chart_command_all(mock_agent_class):
    """Test org chart command for all departments."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "📊 Complete Organization Chart"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, ['org', 'chart'])

    assert result.exit_code == 0
    mock_agent.process_command.assert_called_once_with('get_org_chart', department=None)


@patch('src.cli.main.SocialGraphAgent')
def test_network_insights_command(mock_agent_class):
    """Test network insights command."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "🔍 Network insights for Engineering department"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network', 'insights',
        '--person', 'alice@company.com',
        '--department', 'Engineering'
    ])

    assert result.exit_code == 0
    assert "Network insights" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_daily_report_command(mock_agent_class):
    """Test daily report command."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "📈 Daily Report: 5 new connections, 3 meetings analyzed"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, ['network', 'daily-report'])

    assert result.exit_code == 0
    assert "Daily Report" in result.output


@patch('src.cli.main.InsightsAgent')
def test_recommend_command(mock_agent_class):
    """Test recommend connections command."""
    mock_agent = AsyncMock()
    mock_agent.recommend_connections.return_value = "💡 Recommended: Connect with Charlie (similar interests)"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network', 'recommend',
        '--email', 'alice@company.com',
        '--limit', '5'
    ])

    assert result.exit_code == 0
    assert "Recommended" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_export_data_command_csv(mock_agent_class):
    """Test export data command with CSV format."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "✅ Data exported to ./export in CSV format"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'data', 'export',
        '--format', 'csv',
        '--output', './test_export',
        '--include-sensitive'
    ])

    assert result.exit_code == 0
    assert "exported" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_export_data_command_json(mock_agent_class):
    """Test export data command with JSON format."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "✅ Data exported to ./export in JSON format"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'data', 'export',
        '--format', 'json'
    ])

    assert result.exit_code == 0
    assert "exported" in result.output


@patch('src.cli.main.Neo4jManager')
def test_test_connection_command_success(mock_manager_class):
    """Test connection test command success."""
    mock_manager = AsyncMock()
    mock_manager.connect.return_value = None
    mock_manager.close.return_value = None
    mock_manager_class.return_value = mock_manager

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'test-connection'])

    assert result.exit_code == 0
    assert "Neo4j connection: OK" in result.output


@patch('src.cli.main.Neo4jManager')
def test_test_connection_command_failure(mock_manager_class):
    """Test connection test command failure."""
    mock_manager = AsyncMock()
    mock_manager.connect.side_effect = Exception("Connection refused")
    mock_manager_class.return_value = mock_manager

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'test-connection'])

    assert result.exit_code == 0  # Command doesn't fail, just reports error
    assert "Neo4j connection: FAILED" in result.output
    assert "Connection refused" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_interactive_chat_quit(mock_agent_class):
    """Test interactive chat command with quit."""
    mock_agent = AsyncMock()
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, ['chat'], input='quit\n')

    assert result.exit_code == 0
    assert "Welcome to the Workplace Social Graph AI Agent!" in result.output
    assert "Goodbye!" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_interactive_chat_with_response(mock_agent_class):
    """Test interactive chat command with agent response."""
    mock_agent = AsyncMock()
    mock_agent.chat.return_value = "Hello! I can help you with workplace social graph analysis."
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, ['chat'], input='hello\nquit\n')

    assert result.exit_code == 0
    assert "Hello! I can help you" in result.output


def test_cli_with_config_file():
    """Test CLI with config file option."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a temporary config file
        with open('test_config.env', 'w') as f:
            f.write('NEO4J_URI=bolt://test:7687\n')

        result = runner.invoke(cli, ['--config', 'test_config.env', '--help'])
        assert result.exit_code == 0


def test_org_group_help():
    """Test org group help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['org', '--help'])

    assert result.exit_code == 0
    assert "Organizational structure" in result.output
    assert "chart" in result.output


def test_data_group_help():
    """Test data group help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['data', '--help'])

    assert result.exit_code == 0
    assert "Data management" in result.output
    assert "export" in result.output
    assert "stats" in result.output
