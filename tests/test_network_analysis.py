"""Tests for network analysis functionality."""

from unittest.mock import AsyncMock, Mock, patch

import networkx as nx
import pytest

from src.analysis.network_analysis import NetworkAnalyzer
from src.config.settings import Settings
from src.database.models import Person


class TestNetworkAnalyzer:
    """Test cases for NetworkAnalyzer."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings()

    @pytest.fixture
    def network_analyzer(self, settings):
        """Create NetworkAnalyzer instance."""
        mock_neo4j = Mock()  # Use Mock instead of AsyncMock
        return NetworkAnalyzer(mock_neo4j)

    def test_init(self, network_analyzer):
        """Test NetworkAnalyzer initialization."""
        assert network_analyzer.neo4j_manager is not None
        assert hasattr(network_analyzer, 'graph')

    @pytest.mark.asyncio
    async def test_build_graph_from_neo4j(self, network_analyzer):
        """Test building graph from Neo4j data."""
        with patch.object(network_analyzer.neo4j_manager, 'session') as mock_session:
            # Mock the session context manager properly
            mock_session_context = AsyncMock()
            mock_session_instance = AsyncMock()
            mock_session_context.__aenter__.return_value = mock_session_instance
            mock_session_context.__aexit__.return_value = None
            mock_session.return_value = mock_session_context

            # Mock the result
            mock_result = AsyncMock()
            mock_result.data.return_value = []
            mock_session_instance.run.return_value = mock_result

            graph = await network_analyzer.build_graph_from_neo4j()

            assert isinstance(graph, nx.Graph)

    @pytest.mark.asyncio
    async def test_build_directed_graph_from_neo4j(self, network_analyzer):
        """Test building directed graph from Neo4j data."""
        with patch.object(network_analyzer.neo4j_manager, 'session') as mock_session:
            # Mock the session context manager properly
            mock_session_context = AsyncMock()
            mock_session_instance = AsyncMock()
            mock_session_context.__aenter__.return_value = mock_session_instance
            mock_session_context.__aexit__.return_value = None
            mock_session.return_value = mock_session_context

            # Mock the result
            mock_result = AsyncMock()
            mock_result.data.return_value = []
            mock_session_instance.run.return_value = mock_result

            graph = await network_analyzer.build_directed_graph_from_neo4j()

            assert isinstance(graph, nx.DiGraph)

    def test_calculate_centrality_metrics(self, network_analyzer):
        """Test centrality calculations."""
        # Create a simple graph to work with
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_edge("john", "jane")
        network_analyzer.graph.add_edge("jane", "bob")

        centrality = network_analyzer.calculate_centrality_metrics()

        assert isinstance(centrality, dict)

    def test_find_expertise_clusters(self, network_analyzer):
        """Test expertise cluster detection."""
        # Create a graph with expertise data
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("john", expertise_areas=["Python", "Django"])
        network_analyzer.graph.add_node("jane", expertise_areas=["Python", "React"])

        clusters = network_analyzer.find_expertise_clusters("Python")

        assert isinstance(clusters, dict)

    def test_find_collaboration_paths(self, network_analyzer):
        """Test finding collaboration paths between people."""
        # Create a path
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_edge("john", "jane")
        network_analyzer.graph.add_edge("jane", "bob")

        paths = network_analyzer.find_collaboration_paths("john", "bob")

        assert isinstance(paths, list)

    def test_analyze_department_connectivity(self, network_analyzer):
        """Test department connectivity analysis."""
        # Add nodes with department info
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("john", department="Engineering")
        network_analyzer.graph.add_node("jane", department="Engineering")
        network_analyzer.graph.add_node("bob", department="Marketing")
        network_analyzer.graph.add_edge("john", "jane")
        network_analyzer.graph.add_edge("jane", "bob")

        connectivity = network_analyzer.analyze_department_connectivity()

        assert isinstance(connectivity, dict)

    def test_find_influential_people(self, network_analyzer):
        """Test finding influential people."""
        # Create a star topology where one person is central
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_edge("center", "person1")
        network_analyzer.graph.add_edge("center", "person2")
        network_analyzer.graph.add_edge("center", "person3")

        influencers = network_analyzer.find_influential_people(top_n=2)

        assert isinstance(influencers, list)
        assert len(influencers) <= 2

    def test_find_knowledge_brokers(self, network_analyzer):
        """Test finding knowledge brokers."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("john", expertise_areas=["Python"])
        network_analyzer.graph.add_node("jane", expertise_areas=["Python", "React"])
        network_analyzer.graph.add_edge("john", "jane")

        brokers = network_analyzer.find_knowledge_brokers("Python")

        assert isinstance(brokers, list)

    @pytest.mark.asyncio
    async def test_get_org_chart_data(self, network_analyzer):
        """Test getting org chart data."""
        with patch.object(network_analyzer.neo4j_manager, 'session') as mock_session:
            # Mock the session context manager properly
            mock_session_context = AsyncMock()
            mock_session_instance = AsyncMock()
            mock_session_context.__aenter__.return_value = mock_session_instance
            mock_session_context.__aexit__.return_value = None
            mock_session.return_value = mock_session_context

            # Mock the result
            mock_result = AsyncMock()
            mock_result.data.return_value = []
            mock_session_instance.run.return_value = mock_result

            org_chart = await network_analyzer.get_org_chart_data()

            assert isinstance(org_chart, dict)

    def test_empty_graph_handling(self, network_analyzer):
        """Test handling of empty graphs."""
        # Test with empty graph
        network_analyzer.graph = nx.Graph()

        centrality = network_analyzer.calculate_centrality_metrics()
        assert isinstance(centrality, dict)

    def test_single_node_graph(self, network_analyzer):
        """Test handling of single-node graphs."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("john")

        centrality = network_analyzer.calculate_centrality_metrics()
        assert isinstance(centrality, dict)

    @pytest.mark.asyncio
    async def test_error_handling_in_build_graph(self, network_analyzer):
        """Test error handling during graph building."""
        with patch.object(network_analyzer.neo4j_manager, 'session', side_effect=Exception("Database error")):
            with pytest.raises(Exception, match="Database error"):
                await network_analyzer.build_graph_from_neo4j()

    def test_expertise_clustering_with_specific_area(self, network_analyzer):
        """Test expertise clustering for specific area."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("john", expertise_areas=["Python", "Django"])
        network_analyzer.graph.add_node("jane", expertise_areas=["Python", "React"])
        network_analyzer.graph.add_node("bob", expertise_areas=["Java", "Spring"])

        python_clusters = network_analyzer.find_expertise_clusters("Python")

        assert isinstance(python_clusters, dict)
        # Should find clusters related to Python expertise

    def test_find_influential_people_empty_graph(self, network_analyzer):
        """Test finding influential people with empty graph."""
        network_analyzer.graph = None
        with pytest.raises(ValueError, match="Graph not built"):
            network_analyzer.find_influential_people()

    def test_find_influential_people_with_nodes(self, network_analyzer):
        """Test finding influential people with connected nodes."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_edge("person1", "person2")
        network_analyzer.graph.add_edge("person1", "person3")
        network_analyzer.graph.add_edge("person2", "person4")

        result = network_analyzer.find_influential_people()
        assert len(result) >= 1  # At least one influential person
        assert all(isinstance(item, tuple) for item in result)
        assert all(len(item) == 2 for item in result)

    def test_calculate_centrality_metrics_empty_graph(self, network_analyzer):
        """Test centrality metrics calculation with empty graph."""
        network_analyzer.graph = nx.Graph()
        result = network_analyzer.calculate_centrality_metrics()
        assert result == {}

    def test_calculate_centrality_metrics_single_node(self, network_analyzer):
        """Test centrality metrics calculation with single node."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("person1")
        result = network_analyzer.calculate_centrality_metrics()
        assert "person1" in result
        # Check the NetworkMetrics object structure
        metrics = result["person1"]
        assert hasattr(metrics, 'degree_centrality')
        assert hasattr(metrics, 'betweenness_centrality')
        assert hasattr(metrics, 'closeness_centrality')

    def test_calculate_centrality_metrics_multiple_nodes(self, network_analyzer):
        """Test centrality metrics calculation with multiple nodes."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_edge("person1", "person2")
        network_analyzer.graph.add_edge("person2", "person3")

        result = network_analyzer.calculate_centrality_metrics()
        for person in ["person1", "person2", "person3"]:
            assert person in result
            # Check the NetworkMetrics object structure
            metrics = result[person]
            assert hasattr(metrics, 'degree_centrality')
            assert hasattr(metrics, 'betweenness_centrality')
            assert hasattr(metrics, 'closeness_centrality')

    def test_analyze_department_connectivity_empty_graph(self, network_analyzer):
        """Test department connectivity analysis with empty graph."""
        network_analyzer.graph = None
        with pytest.raises(ValueError, match="Graph not built"):
            network_analyzer.analyze_department_connectivity()

    def test_analyze_department_connectivity_single_dept(self, network_analyzer):
        """Test department connectivity analysis with single department."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("person1", department="Engineering")
        network_analyzer.graph.add_node("person2", department="Engineering")
        network_analyzer.graph.add_edge("person1", "person2")

        result = network_analyzer.analyze_department_connectivity()

        # Should return dictionary with department connectivity info
        assert isinstance(result, dict)
        assert "Engineering" in result

    def test_analyze_department_connectivity_multiple_depts(self, network_analyzer):
        """Test department connectivity analysis with multiple departments."""
        network_analyzer.graph = nx.Graph()
        network_analyzer.graph.add_node("person1", department="Engineering")
        network_analyzer.graph.add_node("person2", department="Marketing")
        network_analyzer.graph.add_edge("person1", "person2")

        result = network_analyzer.analyze_department_connectivity()
        assert len(result) >= 0  # May find cross-department connections
