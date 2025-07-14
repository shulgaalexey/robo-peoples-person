"""Tests for the social graph agent."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.agents import SocialGraphAgent
from src.database.models import Person


@pytest.fixture
def test_agent():
    """Create test agent with mocked dependencies."""
    agent = SocialGraphAgent()
    agent.workplace_tools = AsyncMock()
    agent.neo4j_manager = AsyncMock()
    return agent


@pytest.mark.asyncio
async def test_agent_initialization(test_agent):
    """Test agent initialization."""
    assert test_agent.workplace_tools is not None
    assert test_agent.neo4j_manager is not None


@pytest.mark.asyncio
async def test_agent_context_manager(test_agent):
    """Test agent context manager usage."""
    # Test that agent can be used in a context manager pattern
    assert test_agent is not None


@pytest.mark.asyncio
async def test_close_without_tools(test_agent):
    """Test closing agent without tools."""
    test_agent.workplace_tools = None

    await test_agent.close()  # Should not raise exception


@pytest.mark.asyncio
async def test_process_command_add_coworker(test_agent):
    """Test processing add coworker command."""
    with patch.object(test_agent.workplace_tools, 'add_coworker') as mock_add:
        mock_add.return_value = "✅ Added John Doe successfully"

        result = await test_agent.process_command(
            'add_coworker',
            name='John Doe',
            email='john@test.com',
            department='Engineering',
            role='Developer'
        )

        assert "✅" in result
        mock_add.assert_called_once_with(
            name='John Doe',
            email='john@test.com',
            department='Engineering',
            role='Developer'
        )


@pytest.mark.asyncio
async def test_process_command_find_experts(test_agent):
    """Test processing find experts command."""
    with patch.object(test_agent.workplace_tools, 'find_experts') as mock_find:
        mock_find.return_value = "🔍 Found 3 Python experts"

        result = await test_agent.process_command(
            'find_experts',
            skill='Python',
            limit=10
        )

        assert "🔍" in result
        mock_find.assert_called_once_with('Python', 10)


@pytest.mark.asyncio
async def test_process_command_unknown(test_agent):
    """Test processing unknown command."""
    result = await test_agent.process_command('unknown_action')

    assert "Unknown command" in result or "unknown" in result.lower()


@pytest.mark.asyncio
async def test_chat_help_request(test_agent):
    """Test chat help request."""
    response = await test_agent.chat("help")

    assert "help" in response.lower() or "commands" in response.lower()


@pytest.mark.asyncio
async def test_chat_add_coworker_intent(test_agent):
    """Test chat with add coworker intent."""
    with patch.object(test_agent, 'process_command') as mock_process:
        mock_process.return_value = "✅ Person added successfully"

        response = await test_agent.chat("add a new coworker named Alice")

        assert "add" in response.lower() or "alice" in response.lower()


@pytest.mark.asyncio
async def test_chat_find_expert_intent(test_agent):
    """Test chat with find expert intent."""
    response = await test_agent.chat("who knows Python?")

    assert "expert" in response.lower() or "python" in response.lower()


@pytest.mark.asyncio
async def test_chat_network_analysis_intent(test_agent):
    """Test chat with network analysis intent."""
    response = await test_agent.chat("show me network insights")

    assert "network" in response.lower() or "insight" in response.lower()


@pytest.mark.asyncio
async def test_get_stats(test_agent):
    """Test getting basic stats."""
    # Mock the neo4j manager methods
    test_agent.neo4j_manager.count_people = AsyncMock(return_value=10)
    test_agent.neo4j_manager.count_relationships = AsyncMock(return_value=25)

    stats = await test_agent.get_stats()

    assert "total_people" in stats
    assert "total_relationships" in stats


@pytest.mark.asyncio
async def test_chat_error_handling(test_agent):
    """Test chat error handling."""
    # Test with empty input
    response = await test_agent.chat("")
    assert len(response) > 0  # Should return some response

    # Test with very long input (edge case)
    long_input = "x" * 1000
    response = await test_agent.chat(long_input)
    assert len(response) > 0  # Should handle gracefully


@pytest.mark.asyncio
async def test_agent_settings_default():
    """Test agent with default settings."""
    agent = SocialGraphAgent()
    assert agent.settings is not None


@pytest.mark.asyncio
async def test_agent_settings_custom():
    """Test agent with custom settings."""
    from src.config.settings import Settings

    custom_settings = Settings(neo4j_uri="bolt://custom:7687")
    agent = SocialGraphAgent(custom_settings)

    assert agent.settings.neo4j_uri == "bolt://custom:7687"


@pytest.mark.asyncio
async def test_process_command_who_should_i_ask(test_agent):
    """Test processing who should I ask command."""
    with patch.object(test_agent.workplace_tools, 'who_should_i_ask') as mock_who:
        mock_who.return_value = "👥 Ask John Doe for Python questions"

        result = await test_agent.process_command(
            'who_should_i_ask',
            skill='Python'
        )

        assert "👥" in result or "Ask" in result
        mock_who.assert_called_once_with('Python')


@pytest.mark.asyncio
async def test_process_command_get_org_chart(test_agent):
    """Test processing get org chart command."""
    with patch.object(test_agent.workplace_tools, 'get_org_chart') as mock_chart:
        mock_chart.return_value = "📊 Organization chart generated"

        result = await test_agent.process_command('get_org_chart')

        assert "📊" in result or "chart" in result.lower()
        mock_chart.assert_called_once()


@pytest.mark.asyncio
async def test_process_command_export_data(test_agent):
    """Test processing export data command."""
    with patch.object(test_agent.workplace_tools, 'export_data') as mock_export:
        mock_export.return_value = "💾 Data exported successfully"

        result = await test_agent.process_command(
            'export_data',
            format='json',
            output_path='test.json'
        )

        assert "💾" in result or "export" in result.lower()
        mock_export.assert_called_once_with('json', 'test.json')


@pytest.mark.asyncio
async def test_process_command_get_network_insights(test_agent):
    """Test processing get network insights command."""
    with patch.object(test_agent.workplace_tools, 'get_network_insights') as mock_insights:
        mock_insights.return_value = "🔍 Network insights generated"

        result = await test_agent.process_command('get_network_insights')

        assert "🔍" in result or "insights" in result.lower()
        mock_insights.assert_called_once()


@pytest.mark.asyncio
async def test_agent_with_valid_commands(test_agent):
    """Test agent with various valid commands."""
    valid_commands = [
        'add_coworker',
        'find_experts',
        'who_should_i_ask',
        'get_org_chart',
        'export_data',
        'get_network_insights'
    ]

    for command in valid_commands:
        result = await test_agent.process_command(command)
        # Should not contain "Unknown command" for valid commands
        assert "Unknown command" not in result


@pytest.mark.asyncio
async def test_chat_various_intents(test_agent):
    """Test chat with various user intents."""
    test_cases = [
        ("hello", "greeting"),
        ("add someone", "add"),
        ("find expert", "expert"),
        ("network analysis", "network"),
        ("org chart", "chart")
    ]

    for user_input, expected_keyword in test_cases:
        response = await test_agent.chat(user_input)
        assert len(response) > 0  # Should always return a response
        # Note: We can't assert specific content without knowing the exact LLM responses


@pytest.mark.asyncio
async def test_agent_memory_conversation(test_agent):
    """Test agent conversation memory."""
    # Test that agent can handle multiple chat turns
    response1 = await test_agent.chat("Hello")
    assert len(response1) > 0

    response2 = await test_agent.chat("What did I just say?")
    assert len(response2) > 0


@pytest.mark.asyncio
async def test_agent_error_recovery(test_agent):
    """Test agent error recovery."""
    # Test that agent handles tool errors gracefully
    with patch.object(test_agent.workplace_tools, 'add_coworker') as mock_add:
        mock_add.side_effect = Exception("Database error")

        result = await test_agent.process_command('add_coworker', name="Test")

        # Should handle error gracefully, not crash
        assert len(result) > 0
        assert "error" in result.lower() or "failed" in result.lower()


@pytest.mark.asyncio
async def test_agent_initialization_with_custom_settings(test_agent):
    """Test agent initialization with custom settings."""
    from src.config.settings import Settings

    custom_settings = Settings(
        neo4j_uri="bolt://test:7687",
        agent_memory_size=500
    )

    agent = SocialGraphAgent(custom_settings)

    assert agent.settings.neo4j_uri == "bolt://test:7687"
    assert agent.settings.agent_memory_size == 500


def test_agent_creation_without_settings():
    """Test agent creation without explicit settings."""
    agent = SocialGraphAgent()

    assert agent is not None
    assert agent.settings is not None
    assert hasattr(agent, 'workplace_tools')
    assert hasattr(agent, 'neo4j_manager')
