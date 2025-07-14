"""Test configuration and fixtures."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.agents import InsightsAgent, SocialGraphAgent
from src.config.settings import Settings
from src.database.neo4j_manager import Neo4jManager


@pytest.fixture
def test_settings():
    """Test settings fixture."""
    return Settings(
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j",
        neo4j_password="password",
        neo4j_database="test",
        debug=True
    )


@pytest.fixture
def mock_neo4j_manager():
    """Mock Neo4j manager for testing."""
    manager = AsyncMock(spec=Neo4jManager)
    manager.connect = AsyncMock()
    manager.close = AsyncMock()
    manager.count_people = AsyncMock(return_value=10)
    manager.count_relationships = AsyncMock(return_value=25)
    return manager


@pytest.fixture
async def test_agent(test_settings, mock_neo4j_manager):
    """Test social graph agent fixture."""
    agent = SocialGraphAgent(test_settings)
    agent.neo4j_manager = mock_neo4j_manager
    return agent


@pytest.fixture
async def test_insights_agent(test_settings, mock_neo4j_manager):
    """Test insights agent fixture."""
    agent = InsightsAgent(test_settings)
    agent.neo4j_manager = mock_neo4j_manager
    return agent


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
