"""Tests for the social graph agent."""

from unittest.mock import AsyncMock, patch

import pytest

from src.agents import SocialGraphAgent
from src.database.models import Person


@pytest.mark.asyncio
async def test_agent_initialization(test_settings):
    """Test agent initialization."""
    agent = SocialGraphAgent(test_settings)

    assert agent.settings == test_settings
    assert agent.neo4j_manager is not None
    assert agent.workplace_tools is not None


@pytest.mark.asyncio
async def test_agent_context_manager(test_agent):
    """Test agent as async context manager."""
    async with test_agent as agent:
        assert agent is not None
        # Mock should have been called
        agent.neo4j_manager.connect.assert_called_once()

    # Close should be called on exit
    test_agent.neo4j_manager.close.assert_called_once()


@pytest.mark.asyncio
async def test_process_command_add_coworker(test_agent):
    """Test processing add_coworker command."""
    # Mock the add_coworker_tool function
    with patch('src.agents.social_graph_agent.add_coworker_tool') as mock_tool:
        mock_tool.return_value = "✅ Added John Doe successfully"

        result = await test_agent.process_command(
            "add_coworker",
            name="John Doe",
            email="john@company.com",
            department="Engineering",
            role="Developer"
        )

        assert result == "✅ Added John Doe successfully"
        mock_tool.assert_called_once()


@pytest.mark.asyncio
async def test_process_command_find_experts(test_agent):
    """Test processing find_experts command."""
    with patch('src.agents.social_graph_agent.find_experts_tool') as mock_tool:
        mock_tool.return_value = "🔍 Found 3 Python experts"

        result = await test_agent.process_command(
            "find_experts",
            skill="Python",
            limit=5
        )

        assert result == "🔍 Found 3 Python experts"
        mock_tool.assert_called_once()


@pytest.mark.asyncio
async def test_process_command_unknown(test_agent):
    """Test processing unknown command."""
    result = await test_agent.process_command("unknown_command")

    assert "Unknown command" in result
    assert "unknown_command" in result


@pytest.mark.asyncio
async def test_chat_help_request(test_agent):
    """Test chat with help request."""
    response = await test_agent.chat("help")

    assert "Workplace Social Graph AI Agent Help" in response
    assert "add_coworker" in response
    assert "find_experts" in response


@pytest.mark.asyncio
async def test_chat_add_coworker_intent(test_agent):
    """Test chat with add coworker intent."""
    response = await test_agent.chat("I want to add a new coworker")

    assert "add_coworker" in response
    assert "name" in response
    assert "email" in response


@pytest.mark.asyncio
async def test_chat_find_expert_intent(test_agent):
    """Test chat with find expert intent."""
    response = await test_agent.chat("Who knows Python?")

    assert "find_experts" in response or "expert" in response


@pytest.mark.asyncio
async def test_chat_network_analysis_intent(test_agent):
    """Test chat with network analysis intent."""
    response = await test_agent.chat("Show me network connections")

    assert "network" in response
    assert "get_network_insights" in response


@pytest.mark.asyncio
async def test_get_stats(test_agent):
    """Test getting network statistics."""
    # Mock network analyzer
    mock_analyzer = AsyncMock()
    mock_analyzer.build_graph_from_neo4j = AsyncMock()
    mock_analyzer.analyze_department_connectivity.return_value = {
        "Engineering": {"member_count": 5},
        "Sales": {"member_count": 3}
    }
    mock_analyzer.calculate_network_density.return_value = 0.15

    with patch.object(test_agent.workplace_tools, '_get_network_analyzer', return_value=mock_analyzer):
        stats = await test_agent.get_stats()

        assert stats["total_people"] == 10  # From mock
        assert stats["total_relationships"] == 25  # From mock
        assert stats["total_departments"] == 2
        assert stats["network_density"] == 0.15
        assert stats["largest_department"] == "Engineering"


@pytest.mark.asyncio
async def test_get_stats_error_handling(test_agent):
    """Test error handling in get_stats."""
    # Make neo4j_manager.count_people raise an exception
    test_agent.neo4j_manager.count_people.side_effect = Exception("Database error")

    stats = await test_agent.get_stats()

    assert "error" in stats
    assert "Database error" in stats["error"]


@pytest.mark.asyncio
async def test_chat_error_handling(test_agent):
    """Test error handling in chat method."""
    # Mock process_command to raise an exception
    with patch.object(test_agent, 'process_command', side_effect=Exception("Test error")):
        response = await test_agent.chat("add coworker")

        assert "error" in response.lower()
        assert "Test error" in response
