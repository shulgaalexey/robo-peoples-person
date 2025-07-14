"""Tests for InsightsAgent."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.agents.insights_agent import InsightsAgent
from src.config.settings import Settings
from src.database.models import Person


class TestInsightsAgent:
    """Test cases for InsightsAgent class."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings()

    @pytest.fixture
    def insights_agent(self, settings):
        """Create an InsightsAgent instance for testing."""
        return InsightsAgent(settings)

    def test_init(self, insights_agent, settings):
        """Test InsightsAgent initialization."""
        assert insights_agent.settings == settings
        assert insights_agent.neo4j_manager is not None
        assert insights_agent.network_analyzer is None

    @pytest.mark.asyncio
    async def test_context_manager(self, insights_agent):
        """Test agent as context manager."""
        with patch.object(insights_agent.neo4j_manager, 'connect') as mock_connect, \
             patch.object(insights_agent.neo4j_manager, 'close') as mock_close, \
             patch('src.agents.insights_agent.NetworkAnalyzer') as mock_analyzer_class:

            mock_analyzer = AsyncMock()
            mock_analyzer_class.return_value = mock_analyzer
            mock_analyzer.build_graph_from_neo4j = AsyncMock()

            async with insights_agent as agent:
                assert agent == insights_agent
                assert insights_agent.network_analyzer == mock_analyzer

            mock_connect.assert_called_once()
            mock_analyzer.build_graph_from_neo4j.assert_called_once()
            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_initialize(self, insights_agent):
        """Test initialize method."""
        with patch.object(insights_agent.neo4j_manager, 'connect') as mock_connect, \
             patch('src.agents.insights_agent.NetworkAnalyzer') as mock_analyzer_class:

            mock_analyzer = AsyncMock()
            mock_analyzer_class.return_value = mock_analyzer
            mock_analyzer.build_graph_from_neo4j = AsyncMock()

            await insights_agent.initialize()

            mock_connect.assert_called_once()
            assert insights_agent.network_analyzer == mock_analyzer
            mock_analyzer.build_graph_from_neo4j.assert_called_once()

    @pytest.mark.asyncio
    async def test_close(self, insights_agent):
        """Test close method."""
        with patch.object(insights_agent.neo4j_manager, 'close') as mock_close:
            await insights_agent.close()
            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_network_loaded(self, insights_agent):
        """Test _ensure_network_loaded method."""
        # Test when network_analyzer is None
        assert insights_agent.network_analyzer is None

        with patch('src.agents.insights_agent.NetworkAnalyzer') as mock_analyzer_class:
            mock_analyzer = AsyncMock()
            mock_analyzer_class.return_value = mock_analyzer
            mock_analyzer.build_graph_from_neo4j = AsyncMock()

            await insights_agent._ensure_network_loaded()

            assert insights_agent.network_analyzer == mock_analyzer
            mock_analyzer.build_graph_from_neo4j.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_daily_insights(self, insights_agent):
        """Test daily insights generation."""
        # Mock network analyzer properly
        mock_analyzer = Mock()
        mock_graph = Mock()
        # Mock graph nodes and edges as methods that return lists that can be used with len()
        mock_graph.nodes = Mock(return_value=["node1", "node2", "node3"])
        mock_graph.edges = Mock(return_value=[("node1", "node2"), ("node2", "node3")])
        mock_analyzer.graph = mock_graph
        mock_analyzer.calculate_network_density.return_value = 0.67
        mock_analyzer.analyze_department_connectivity.return_value = {
            "Engineering": {"member_count": 10, "external_connections": 20, "internal_density": 0.8}
        }
        # Mock the correct method: find_influential_people, not find_bridge_people
        mock_analyzer.find_influential_people.return_value = [("Jane Smith", 0.9)]
        insights_agent.network_analyzer = mock_analyzer

        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure, \
             patch.object(insights_agent, '_calculate_network_health', return_value=0.8) as mock_health, \
             patch.object(insights_agent, '_generate_recommendations', return_value=["Test recommendation"]) as mock_recs:

            result = await insights_agent.generate_daily_insights()

            assert "📊" in result
            assert "network health" in result.lower()
            mock_ensure.assert_called_once()
            mock_health.assert_called_once()
            mock_recs.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns(self, insights_agent):
        """Test collaboration pattern analysis."""
        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure, \
             patch.object(insights_agent.neo4j_manager, 'session') as mock_session_cm:

            mock_session = AsyncMock()
            mock_session_cm.return_value.__aenter__.return_value = mock_session
            mock_session_cm.return_value.__aexit__.return_value = None

            mock_result = AsyncMock()
            mock_result.data.return_value = []
            mock_session.run.return_value = mock_result

            result = await insights_agent.analyze_collaboration_patterns()

            assert "🤝" in result
            assert "collaboration" in result.lower()
            mock_ensure.assert_called_once()

    @pytest.mark.asyncio
    async def test_identify_silos(self, insights_agent):
        """Test silo identification."""
        # Mock network analyzer properly
        mock_analyzer = Mock()
        # Make find_communities return a simple list (the code wraps it in list() anyway)
        mock_communities = [["person1", "person2"], ["person3"]]
        mock_analyzer.find_communities.return_value = mock_communities
        mock_analyzer.analyze_department_connectivity.return_value = {
            "IT": {"external_connections": 2, "member_count": 10},
            "HR": {"external_connections": 1, "member_count": 5}
        }
        # Mock find_bridge_people method that's also called in this method
        mock_analyzer.find_bridge_people.return_value = [("John Bridge", 0.8)]
        insights_agent.network_analyzer = mock_analyzer

        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure, \
             patch.object(insights_agent, '_generate_silo_reduction_suggestions', return_value=["Test suggestion"]) as mock_suggestions, \
             patch.object(insights_agent.neo4j_manager, 'session') as mock_session_cm:

            mock_session = AsyncMock()
            mock_session_cm.return_value.__aenter__.return_value = mock_session
            mock_session_cm.return_value.__aexit__.return_value = None

            # Mock department query result
            mock_result = AsyncMock()
            mock_result.data.return_value = [
                {"department": "Engineering", "internal_connections": 10, "external_connections": 2}
            ]
            mock_session.run.return_value = mock_result

            result = await insights_agent.identify_silos()

            assert "Organizational Silo Analysis" in result
            assert "silo" in result.lower()
            mock_ensure.assert_called_once()

    @pytest.mark.asyncio
    async def test_recommend_connections_success(self, insights_agent):
        """Test successful connection recommendations."""
        # Mock dependencies
        mock_analyzer = Mock()
        insights_agent.network_analyzer = mock_analyzer

        # Mock person lookup
        test_person = Person(
            name="John Doe",
            email="john@test.com",
            department="Engineering",
            role="Developer"
        )
        test_person.expertise_areas = []  # Make it iterable

        with patch.object(insights_agent.neo4j_manager, 'find_person_by_email', return_value=test_person) as mock_find, \
             patch.object(insights_agent.neo4j_manager, 'get_person_relationships', return_value=[]) as mock_relationships, \
             patch.object(insights_agent.neo4j_manager, 'find_people_by_department', return_value=[]) as mock_dept, \
             patch.object(insights_agent.neo4j_manager, 'find_experts', return_value=[]) as mock_experts, \
             patch.object(insights_agent.neo4j_manager, 'find_cross_department_connectors', return_value=[]) as mock_connectors, \
             patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure:

            result = await insights_agent.recommend_connections("john@test.com", limit=3)

            assert "🤝" in result
            assert "John Doe" in result
            mock_find.assert_called_once_with("john@test.com")
            mock_ensure.assert_called_once()

    @pytest.mark.asyncio
    async def test_recommend_connections_person_not_found(self, insights_agent):
        """Test connection recommendations when person not found."""
        with patch.object(insights_agent.neo4j_manager, 'find_person_by_email', return_value=None) as mock_find, \
             patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure:

            result = await insights_agent.recommend_connections("notfound@test.com")

            assert "❌" in result
            assert "not found" in result.lower()
            mock_find.assert_called_once_with("notfound@test.com")
            mock_ensure.assert_called_once()
