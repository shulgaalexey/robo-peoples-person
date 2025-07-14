"""Tests for InsightsAgent with improved coverage."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.agents.insights_agent import InsightsAgent, create_insights_agent
from src.config.settings import Settings
from src.database.models import Interaction, Person


class TestInsightsAgent:
    """Test cases for InsightsAgent class."""

    @pytest.fixture
    async def insights_agent(self):
        """Create InsightsAgent for testing."""
        settings = Settings()
        agent = InsightsAgent(settings)
        agent.neo4j_manager = AsyncMock()
        agent.network_analyzer = Mock()
        return agent

    @pytest.fixture
    def sample_interactions(self):
        """Sample interactions for testing."""
        return [
            Mock(person1_email="john@company.com", person2_email="jane@company.com", strength=0.8, timestamp=datetime.now()),
            Mock(person1_email="bob@company.com", person2_email="alice@company.com", strength=0.6, timestamp=datetime.now())
        ]

    @pytest.mark.asyncio
    async def test_init(self):
        """Test InsightsAgent initialization."""
        settings = Settings()
        agent = InsightsAgent(settings)
        assert agent.settings == settings
        assert agent.neo4j_manager is not None
        assert agent.network_analyzer is None  # Initially None until initialize() is called

    @pytest.mark.asyncio
    async def test_init_with_default_settings(self):
        """Test InsightsAgent initialization with default settings."""
        agent = InsightsAgent()
        assert agent.settings is not None
        assert agent.neo4j_manager is not None
        assert agent.network_analyzer is None  # Initially None until initialize() is called

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test InsightsAgent as context manager."""
        settings = Settings()

        with patch('src.agents.insights_agent.Neo4jManager') as mock_neo4j_class:
            mock_neo4j = AsyncMock()
            mock_neo4j_class.return_value = mock_neo4j
            mock_neo4j.connect = AsyncMock()
            mock_neo4j.close = AsyncMock()

            with patch('src.agents.insights_agent.NetworkAnalyzer') as mock_analyzer_class:
                mock_analyzer = Mock()
                mock_analyzer.build_graph_from_neo4j = AsyncMock()
                mock_analyzer_class.return_value = mock_analyzer

                async with InsightsAgent(settings) as agent:
                    assert agent.settings == settings
                    mock_neo4j.connect.assert_called_once()

                mock_neo4j.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_initialize(self, insights_agent):
        """Test agent initialization."""
        with patch.object(insights_agent.neo4j_manager, 'connect') as mock_connect:
            mock_connect.return_value = AsyncMock()

            with patch('src.agents.insights_agent.NetworkAnalyzer') as mock_analyzer_class:
                mock_analyzer = Mock()
                mock_analyzer.build_graph_from_neo4j = AsyncMock()
                mock_analyzer_class.return_value = mock_analyzer

                await insights_agent.initialize()

                mock_connect.assert_called_once()
                mock_analyzer.build_graph_from_neo4j.assert_called_once()

    @pytest.mark.asyncio
    async def test_close(self, insights_agent):
        """Test agent closure."""
        with patch.object(insights_agent.neo4j_manager, 'close') as mock_close:
            await insights_agent.close()
            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_daily_insights(self, insights_agent):
        """Test daily insights generation."""
        # Create a mock graph with proper structure
        mock_graph = Mock()
        mock_graph.nodes.return_value = ['Alice', 'Bob', 'Charlie']  # Return list of nodes
        mock_graph.edges.return_value = [('Alice', 'Bob'), ('Bob', 'Charlie')]  # Return list of edges

        # Mock network analyzer with properly configured methods
        mock_analyzer = Mock()
        mock_analyzer.graph = mock_graph
        mock_analyzer.calculate_network_density.return_value = 0.67
        mock_analyzer.find_influential_people.return_value = [("Alice", 0.8), ("Bob", 0.6)]
        mock_analyzer.analyze_department_connectivity.return_value = {
            "Engineering": {"internal_density": 0.8}
        }

        insights_agent.network_analyzer = mock_analyzer

        # Mock all methods that are called
        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure, \
             patch.object(insights_agent, '_calculate_network_health', return_value=0.75) as mock_health, \
             patch.object(insights_agent, '_generate_recommendations', return_value=["Connect with teammates"]) as mock_recs:

            result = await insights_agent.generate_daily_insights()

            assert "📊" in result
            assert "network health" in result.lower()
            mock_ensure.assert_called()
            mock_health.assert_called_once()
            mock_recs.assert_called_once()

    @pytest.mark.asyncio
    async def test_calculate_network_health(self, insights_agent):
        """Test network health calculation."""
        # Mock network data
        mock_people = [
            Mock(name="John Doe", email="john@company.com"),
            Mock(name="Jane Smith", email="jane@company.com"),
            Mock(name="Bob Wilson", email="bob@company.com")
        ]
        mock_interactions = [
            Mock(person1_email="john@company.com", person2_email="jane@company.com", strength=0.8),
            Mock(person1_email="jane@company.com", person2_email="bob@company.com", strength=0.6)
        ]

        insights_agent.neo4j_manager.get_all_people.return_value = mock_people
        insights_agent.neo4j_manager.get_recent_interactions.return_value = mock_interactions
        insights_agent.network_analyzer.calculate_network_density.return_value = 0.67
        insights_agent.network_analyzer.find_influential_people.return_value = [("John Doe", 0.8)]
        insights_agent.network_analyzer.analyze_department_connectivity.return_value = {
            "Engineering": {"member_count": 10, "external_connections": 20},
            "Sales": {"member_count": 8, "external_connections": 16}
        }
        insights_agent.network_analyzer.find_bridge_people.return_value = [("Jane Smith", 0.9)]

        result = await insights_agent._calculate_network_health()

        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns(self, insights_agent, sample_interactions):
        """Test collaboration pattern analysis."""
        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure, \
             patch.object(insights_agent.neo4j_manager, 'get_recent_interactions', return_value=sample_interactions) as mock_interactions, \
             patch.object(insights_agent, '_analyze_cross_department_collaboration', return_value={("Engineering", "Sales"): 5}) as mock_cross, \
             patch.object(insights_agent, '_analyze_collaboration_trends', return_value=["Increasing collaboration"]) as mock_trends:

            result = await insights_agent.analyze_collaboration_patterns()

            assert "🤝" in result
            assert "collaboration" in result.lower()
            mock_ensure.assert_called_once()
            mock_interactions.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns_no_interactions(self, insights_agent):
        """Test collaboration pattern analysis with no interactions."""
        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure, \
             patch.object(insights_agent.neo4j_manager, 'get_recent_interactions', return_value=[]) as mock_interactions:

            result = await insights_agent.analyze_collaboration_patterns()

            assert "🤝" in result
            assert "collaboration" in result.lower()

    @pytest.mark.asyncio
    async def test_identify_silos(self, insights_agent):
        """Test silo identification."""
        # Mock network analyzer with proper return values (not async for find_communities)
        mock_analyzer = Mock()
        mock_analyzer.find_communities.return_value = [["person1", "person2"], ["person3"]]
        mock_analyzer.analyze_department_connectivity.return_value = {
            "IT": {"external_connections": 2, "member_count": 10},
            "HR": {"external_connections": 8, "member_count": 5}
        }
        mock_analyzer.find_bridge_people.return_value = [("John Doe", 0.8)]
        insights_agent.network_analyzer = mock_analyzer

        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure, \
             patch.object(insights_agent, '_generate_silo_reduction_suggestions', return_value=["Create cross-team projects"]) as mock_suggestions:

            result = await insights_agent.identify_silos()

            assert "🏗️" in result
            assert "silos" in result.lower() or "communities" in result.lower()
            mock_ensure.assert_called_once()

    @pytest.mark.asyncio
    async def test_identify_silos_no_silos(self, insights_agent):
        """Test silo identification when no silos found."""
        mock_analyzer = Mock()
        mock_analyzer.find_communities.return_value = [["person1", "person2", "person3"]]  # Single community
        mock_analyzer.analyze_department_connectivity.return_value = {
            "Engineering": {"external_connections": 15, "member_count": 5},
            "Sales": {"external_connections": 20, "member_count": 8}
        }
        mock_analyzer.find_bridge_people.return_value = []
        insights_agent.network_analyzer = mock_analyzer

        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure:
            result = await insights_agent.identify_silos()

            assert "🏗️" in result
            mock_ensure.assert_called_once()

    @pytest.mark.asyncio
    async def test_recommend_connections_success(self, insights_agent):
        """Test connection recommendations for valid person."""
        mock_person = Mock(name="John Doe", email="john@company.com", department="Engineering")
        mock_person.expertise_areas = []  # Make it iterable
        insights_agent.neo4j_manager.find_person_by_email.return_value = mock_person
        insights_agent.neo4j_manager.get_person_relationships.return_value = []
        insights_agent.neo4j_manager.find_people_by_department.return_value = []
        insights_agent.neo4j_manager.find_experts.return_value = []
        insights_agent.neo4j_manager.find_cross_department_connectors.return_value = []

        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure:
            result = await insights_agent.recommend_connections("john@company.com")

            assert "🤝" in result
            assert "John Doe" in result
            mock_ensure.assert_called_once()

    @pytest.mark.asyncio
    async def test_recommend_connections_person_not_found(self, insights_agent):
        """Test connection recommendations for non-existent person."""
        insights_agent.neo4j_manager.find_person_by_email.return_value = None

        with patch.object(insights_agent, '_ensure_network_loaded') as mock_ensure:
            result = await insights_agent.recommend_connections("nonexistent@company.com")

            assert "❌" in result
            assert "not found" in result.lower()

    @pytest.mark.asyncio
    async def test_ensure_network_loaded_already_loaded(self, insights_agent):
        """Test network loading when already loaded."""
        mock_analyzer = AsyncMock()
        insights_agent.network_analyzer = mock_analyzer

        await insights_agent._ensure_network_loaded()

        # Should still call build_graph_from_neo4j as per implementation
        mock_analyzer.build_graph_from_neo4j.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_network_loaded_not_loaded(self, insights_agent):
        """Test network loading when not loaded."""
        insights_agent.network_analyzer.graph = None
        mock_analyzer = AsyncMock()
        insights_agent.network_analyzer = mock_analyzer

        await insights_agent._ensure_network_loaded()

        mock_analyzer.build_graph_from_neo4j.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_recommendations(self, insights_agent):
        """Test recommendation generation."""
        # Mock network analyzer with proper sync methods
        mock_analyzer = Mock()
        mock_analyzer.calculate_network_density.return_value = 0.3  # Low density
        mock_analyzer.analyze_department_connectivity.return_value = {
            "IT": {"external_connections": 2, "member_count": 10}
        }
        mock_analyzer.find_bridge_people.return_value = [("John", 0.8)]
        insights_agent.network_analyzer = mock_analyzer

        recommendations = await insights_agent._generate_recommendations()

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

    @pytest.mark.asyncio
    async def test_analyze_cross_department_collaboration(self, insights_agent, sample_interactions):
        """Test cross-department collaboration analysis."""
        # Mock person lookups to avoid database connections
        mock_persons = {
            "john@company.com": Person(name="John Smith", email="john@company.com", department="Engineering"),
            "jane@company.com": Person(name="Jane Smith", email="jane@company.com", department="Sales"),
            "bob@company.com": Person(name="Bob Wilson", email="bob@company.com", department="Marketing"),
            "alice@company.com": Person(name="Alice Brown", email="alice@company.com", department="Engineering")
        }

        async def mock_find_person(email):
            return mock_persons.get(email)

        with patch.object(insights_agent.neo4j_manager, 'find_person_by_email', side_effect=mock_find_person):
            result = await insights_agent._analyze_cross_department_collaboration(sample_interactions)

            assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_analyze_collaboration_trends(self, insights_agent, sample_interactions):
        """Test collaboration trends analysis."""
        result = await insights_agent._analyze_collaboration_trends(sample_interactions)

        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_generate_silo_reduction_suggestions(self, insights_agent):
        """Test silo reduction suggestions generation."""
        isolated_depts = ["IT", "HR"]

        suggestions = await insights_agent._generate_silo_reduction_suggestions(isolated_depts)

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0


@pytest.mark.asyncio
async def test_create_insights_agent():
    """Test create_insights_agent function."""
    with patch('src.agents.insights_agent.InsightsAgent') as mock_agent_class:
        mock_agent = AsyncMock()
        mock_agent_class.return_value = mock_agent

        result = await create_insights_agent()

        mock_agent_class.assert_called_once_with(None)
        mock_agent.initialize.assert_called_once()
        assert result == mock_agent


@pytest.mark.asyncio
async def test_create_insights_agent_with_settings():
    """Test create_insights_agent function with custom settings."""
    custom_settings = Settings()

    with patch('src.agents.insights_agent.InsightsAgent') as mock_agent_class:
        mock_agent = AsyncMock()
        mock_agent_class.return_value = mock_agent

        result = await create_insights_agent(custom_settings)

        mock_agent_class.assert_called_once_with(custom_settings)
        mock_agent.initialize.assert_called_once()
        assert result == mock_agent
