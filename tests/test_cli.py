"""Tests for CLI functionality."""

from unittest.mock import AsyncMock, Mock, patch

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
    mock_agent.process_command.return_value = "🤔 Ask Sarah Johnson about Machine Learning"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'person', 'who-to-ask',
        '--topic', 'Machine Learning'
    ])

    assert result.exit_code == 0
    assert "Ask Sarah Johnson about Machine Learning" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_org_chart_command(mock_agent_class):
    """Test org chart command."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "📊 Engineering Org Chart:\nJohn Smith (Manager)"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'org', 'chart',
        '--department', 'Engineering'
    ])

    assert result.exit_code == 0
    assert "Engineering Org Chart" in result.output


@patch('src.cli.main.SocialGraphAgent')
def test_network_insights_command(mock_agent_class):
    """Test network insights command."""
    mock_agent = AsyncMock()
    mock_agent.process_command.return_value = "📈 Network insights for john@company.com"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network', 'insights',
        '--person', 'john@company.com'
    ])

    assert result.exit_code == 0
    assert "Network insights for john@company.com" in result.output


@patch('src.cli.main.InsightsAgent')
def test_daily_report_command(mock_agent_class):
    """Test daily report command."""
    mock_agent = AsyncMock()
    mock_agent.generate_daily_insights.return_value = "📊 Daily Network Report: 50 people, 200 interactions"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network', 'daily-report'
    ])

    assert result.exit_code == 0
    assert "Daily Network Report" in result.output


@patch('src.cli.main.InsightsAgent')
def test_collaboration_command(mock_agent_class):
    """Test collaboration analysis command."""
    mock_agent = AsyncMock()
    mock_agent.analyze_collaboration_patterns.return_value = "🤝 Collaboration patterns: High cross-team interaction"
    mock_agent.__aenter__.return_value = mock_agent
    mock_agent.__aexit__.return_value = None
    mock_agent_class.return_value = mock_agent

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network', 'collaboration',
        '--days', '14'
    ])

    assert result.exit_code == 0
    assert "Collaboration patterns" in result.output


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


@patch('src.database.neo4j_manager.Neo4jManager')
def test_test_connection_command_success(mock_manager_class):
    """Test connection test command success."""
    mock_manager = AsyncMock()
    mock_manager.connect.return_value = None
    mock_manager.close.return_value = None
    mock_manager_class.return_value = mock_manager

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'check-config'])

    assert result.exit_code == 0
    assert "Neo4j connection: OK" in result.output


@patch('src.database.neo4j_manager.Neo4jManager')
def test_test_connection_command_failure(mock_manager_class):
    """Test connection test command failure."""
    mock_manager = AsyncMock()
    mock_manager.connect.side_effect = Exception("Connection refused")
    mock_manager_class.return_value = mock_manager

    runner = CliRunner()
    result = runner.invoke(cli, ['setup', 'check-config'])

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


def test_cli_with_config_file(tmp_path):
    """Test CLI with config file parameter."""
    runner = CliRunner()
    # Create a temporary config file
    config_file = tmp_path / "test_config.env"
    config_file.write_text("NEO4J_URI=bolt://test:7687\nNEO4J_USER=test\nNEO4J_PASSWORD=test")

    # Test that the CLI accepts the config parameter
    result = runner.invoke(cli, ['--config', str(config_file), '--help'])
    assert result.exit_code == 0
    assert "Path to configuration file" in result.output


def test_cli_without_config_file():
    """Test CLI without config file parameter uses default settings."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Workplace Social Graph AI Agent CLI" in result.output


@patch('asyncio.run')
@patch('src.cli.main.InsightsAgent')
def test_network_silos_command(mock_agent_class, mock_asyncio):
    """Test network silos command."""
    runner = CliRunner()
    mock_agent = AsyncMock()
    mock_agent.identify_silos.return_value = "Silos analysis result"
    mock_agent_class.return_value.__aenter__.return_value = mock_agent
    mock_agent_class.return_value.__aexit__.return_value = None

    result = runner.invoke(cli, ['network', 'silos'])

    assert result.exit_code == 0
    mock_asyncio.assert_called_once()


@patch('asyncio.run')
@patch('src.cli.main.InsightsAgent')
def test_network_recommend_connections_command(mock_agent_class, mock_asyncio):
    """Test network recommend connections command."""
    runner = CliRunner()
    mock_agent = AsyncMock()
    mock_agent.recommend_connections.return_value = "Connection recommendations"
    mock_agent_class.return_value.__aenter__.return_value = mock_agent
    mock_agent_class.return_value.__aexit__.return_value = None

    result = runner.invoke(cli, ['network', 'recommend-connections', '--email', 'test@example.com', '--limit', '3'])

    assert result.exit_code == 0
    mock_asyncio.assert_called_once()
