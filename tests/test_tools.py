"""Tests for workplace tools functionality."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.agents.tools import (WorkplaceTools, add_coworker_tool,
                              add_relationship_tool, export_data_tool,
                              find_experts_tool, get_network_insights_tool,
                              get_org_chart_tool, log_interaction_tool,
                              who_should_i_ask_tool)
from src.database.models import Interaction, Person, WorkRelationship


class TestWorkplaceTools:
    """Test cases for WorkplaceTools."""

    @pytest.fixture
    def workplace_tools(self):
        """Create WorkplaceTools instance."""
        mock_manager = AsyncMock()
        return WorkplaceTools(mock_manager)

    def test_init(self, workplace_tools):
        """Test WorkplaceTools initialization."""
        assert workplace_tools.neo4j_manager is not None
        assert workplace_tools.network_analyzer is None
        assert workplace_tools.export_manager is None

    @pytest.mark.asyncio
    async def test_get_neo4j_manager(self, workplace_tools):
        """Test getting Neo4j manager."""
        manager = await workplace_tools._get_neo4j_manager()
        assert manager is not None

    @pytest.mark.asyncio
    async def test_get_network_analyzer(self, workplace_tools):
        """Test getting network analyzer."""
        with patch('src.agents.tools.NetworkAnalyzer') as mock_analyzer:
            mock_instance = AsyncMock()
            mock_analyzer.return_value = mock_instance

            analyzer = await workplace_tools._get_network_analyzer()
            assert analyzer == mock_instance

    @pytest.mark.asyncio
    async def test_get_export_manager(self, workplace_tools):
        """Test getting export manager."""
        with patch('src.agents.tools.ExportManager') as mock_manager:
            mock_instance = AsyncMock()
            mock_manager.return_value = mock_instance

            manager = await workplace_tools._get_export_manager()
            assert manager == mock_instance


class TestToolFunctions:
    """Test cases for tool functions."""

    @pytest.fixture
    def workplace_tools(self):
        """Create mocked WorkplaceTools."""
        mock_tools = AsyncMock()
        mock_manager = AsyncMock()
        mock_tools._get_neo4j_manager.return_value = mock_manager
        return mock_tools

    @pytest.mark.asyncio
    async def test_add_coworker_tool_success(self, workplace_tools):
        """Test successful coworker addition."""
        workplace_tools._get_neo4j_manager.return_value.add_coworker.return_value = "Person John Doe created successfully"

        result = await add_coworker_tool(
            workplace_tools,
            name="John Doe",
            email="john@test.com",
            department="Engineering",
            role="Developer"
        )

        assert "✅" in result
        assert "John Doe" in result

    @pytest.mark.asyncio
    async def test_add_coworker_tool_failure(self, workplace_tools):
        """Test coworker addition failure."""
        workplace_tools._get_neo4j_manager.return_value.add_coworker.side_effect = Exception("Database error")

        result = await add_coworker_tool(
            workplace_tools,
            name="John Doe",
            email="john@test.com"
        )

        assert "❌" in result
        assert "Database error" in result

    @pytest.mark.asyncio
    async def test_find_experts_tool_success(self, workplace_tools):
        """Test successful expert finding."""
        mock_experts = [
            Person(name="Jane Doe", email="jane@test.com", department="Engineering", expertise=["Python"])
        ]
        workplace_tools._get_neo4j_manager.return_value.find_experts.return_value = mock_experts

        result = await find_experts_tool(
            workplace_tools,
            expertise_area="Python",
            limit=5
        )

        assert "🎯" in result
        assert "Jane Doe" in result

    @pytest.mark.asyncio
    async def test_find_experts_tool_no_results(self, workplace_tools):
        """Test expert finding with no results."""
        workplace_tools._get_neo4j_manager.return_value.find_experts.return_value = []

        result = await find_experts_tool(
            workplace_tools,
            expertise_area="Nonexistent Skill"
        )

        assert "No experts found" in result

    @pytest.mark.asyncio
    async def test_who_should_i_ask_tool(self, workplace_tools):
        """Test who should I ask tool."""
        mock_experts = [
            Person(name="Expert User", email="expert@test.com", department="Engineering")
        ]
        workplace_tools._get_neo4j_manager.return_value.find_experts.return_value = mock_experts

        result = await who_should_i_ask_tool(
            workplace_tools,
            question_topic="Python debugging"
        )

        assert len(result) > 0
        # Result format may vary, just check it's not empty

    @pytest.mark.asyncio
    async def test_get_org_chart_tool(self, workplace_tools):
        """Test org chart tool."""
        mock_people = [
            Person(name="Manager", email="mgr@test.com", department="Engineering", role="Manager"),
            Person(name="Developer", email="dev@test.com", department="Engineering", role="Developer")
        ]
        workplace_tools._get_neo4j_manager.return_value.get_people_by_department.return_value = mock_people

        result = await get_org_chart_tool(workplace_tools, department="Engineering")

        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_export_data_tool(self, workplace_tools):
        """Test export data tool."""
        mock_export_manager = AsyncMock()
        mock_export_manager.export_to_json.return_value = "/path/to/export"
        workplace_tools._get_export_manager.return_value = mock_export_manager

        result = await export_data_tool(
            workplace_tools,
            format="json",
            output_path="/test/path"
        )

        assert "💾" in result or "export" in result.lower()

    @pytest.mark.asyncio
    async def test_get_network_insights_tool(self, workplace_tools):
        """Test network insights tool."""
        mock_analyzer = AsyncMock()
        mock_analyzer.analyze_person_centrality.return_value = {"centrality": 0.5}
        mock_analyzer.analyze_department_connectivity.return_value = {"dept": {"connections": 10}}
        workplace_tools._get_network_analyzer.return_value = mock_analyzer

        result = await get_network_insights_tool(workplace_tools)

        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_add_relationship_tool_success(self, workplace_tools):
        """Test successful relationship addition."""
        workplace_tools._get_neo4j_manager.return_value.add_relationship.return_value = True

        result = await add_relationship_tool(
            workplace_tools,
            from_person="John Doe",
            to_person="Jane Smith",
            relationship_type="colleague",
            context="Same team",
            strength=0.8
        )

        assert "✅" in result
        assert "John Doe" in result and "Jane Smith" in result

    @pytest.mark.asyncio
    async def test_add_relationship_tool_invalid_type(self, workplace_tools):
        """Test relationship addition with invalid type."""
        result = await add_relationship_tool(
            workplace_tools,
            from_person="John Doe",
            to_person="Jane Smith",
            relationship_type="invalid_type"
        )

        assert "❌" in result
        assert "Invalid relationship type" in result

    @pytest.mark.asyncio
    async def test_add_relationship_tool_failure(self, workplace_tools):
        """Test relationship addition failure."""
        workplace_tools._get_neo4j_manager.return_value.add_relationship.side_effect = Exception("Database error")

        result = await add_relationship_tool(
            workplace_tools,
            from_person="John Doe",
            to_person="Jane Smith",
            relationship_type="colleague"
        )

        assert "❌" in result
        assert "Database error" in result

    @pytest.mark.asyncio
    async def test_log_interaction_tool_success(self, workplace_tools):
        """Test successful interaction logging."""
        workplace_tools._get_neo4j_manager.return_value.add_interaction.return_value = True

        result = await log_interaction_tool(
            workplace_tools,
            with_person="Jane Smith",
            interaction_type="meeting",
            duration_minutes=30,
            location="Conference Room A",
            notes="Project discussion"
        )

        assert "✅" in result
        assert "logged" in result.lower()

    @pytest.mark.asyncio
    async def test_log_interaction_tool_invalid_type(self, workplace_tools):
        """Test interaction logging with invalid type."""
        result = await log_interaction_tool(
            workplace_tools,
            with_person="Jane Smith",
            interaction_type="invalid_type"
        )

        assert "❌" in result
        assert "Invalid interaction type" in result

    @pytest.mark.asyncio
    async def test_log_interaction_tool_failure(self, workplace_tools):
        """Test interaction logging failure."""
        workplace_tools._get_neo4j_manager.return_value.add_interaction.side_effect = Exception("Database error")

        result = await log_interaction_tool(
            workplace_tools,
            with_person="Jane Smith",
            interaction_type="meeting"
        )

        assert "❌" in result
        assert "Database error" in result


class TestWorkplaceToolsMethods:
    """Test cases for WorkplaceTools class methods."""

    @pytest.fixture
    def workplace_tools(self):
        """Create WorkplaceTools instance with mocked manager."""
        mock_manager = AsyncMock()
        return WorkplaceTools(mock_manager)

    @pytest.mark.asyncio
    async def test_add_coworker_method_success(self, workplace_tools):
        """Test WorkplaceTools.add_coworker method success."""
        workplace_tools.neo4j_manager.add_coworker.return_value = "person_123"

        result = await workplace_tools.add_coworker(
            name="John Doe",
            email="john@test.com",
            department="Engineering",
            role="Developer"
        )

        assert "✅" in result
        assert "John Doe" in result

    @pytest.mark.asyncio
    async def test_add_coworker_method_failure(self, workplace_tools):
        """Test WorkplaceTools.add_coworker method failure."""
        workplace_tools.neo4j_manager.add_coworker.side_effect = Exception("Database error")

        result = await workplace_tools.add_coworker(
            name="John Doe",
            email="john@test.com"
        )

        assert "❌" in result
        assert "Database error" in result

    @pytest.mark.asyncio
    async def test_find_experts_method_success(self, workplace_tools):
        """Test WorkplaceTools.find_experts method success."""
        mock_experts = [
            Person(name="Jane Doe", email="jane@test.com", department="Engineering", expertise_areas=["Python"])
        ]
        workplace_tools.neo4j_manager.find_experts.return_value = mock_experts

        result = await workplace_tools.find_experts(
            expertise_area="Python",
            limit=5
        )

        assert "🎯" in result
        assert "Jane Doe" in result
        assert "Python" in result

    @pytest.mark.asyncio
    async def test_find_experts_method_no_results(self, workplace_tools):
        """Test WorkplaceTools.find_experts method with no results."""
        workplace_tools.neo4j_manager.find_experts.return_value = []

        result = await workplace_tools.find_experts(expertise_area="Nonexistent Skill")

        assert "🎯" in result
        assert "Found 0 expert(s)" in result

    @pytest.mark.asyncio
    async def test_find_experts_method_failure(self, workplace_tools):
        """Test WorkplaceTools.find_experts method failure."""
        workplace_tools.neo4j_manager.find_experts.side_effect = Exception("Database error")

        result = await workplace_tools.find_experts(expertise_area="Python")

        assert "❌" in result
        assert "Database error" in result

    @pytest.mark.asyncio
    async def test_who_should_i_ask_method_success(self, workplace_tools):
        """Test WorkplaceTools.who_should_i_ask method success."""
        mock_experts = [
            Person(name="Expert User", email="expert@test.com", department="Engineering", expertise_areas=["Python"])
        ]
        workplace_tools.neo4j_manager.find_experts.return_value = mock_experts

        result = await workplace_tools.who_should_i_ask(question_topic="Python debugging")

        assert "🤔" in result or "expert" in result.lower()

    @pytest.mark.asyncio
    async def test_who_should_i_ask_method_failure(self, workplace_tools):
        """Test WorkplaceTools.who_should_i_ask method failure."""
        workplace_tools.neo4j_manager.find_experts.side_effect = Exception("Database error")

        result = await workplace_tools.who_should_i_ask(question_topic="Python debugging")

        assert "❌" in result
        assert "Database error" in result

    @pytest.mark.asyncio
    async def test_get_org_chart_method_success(self, workplace_tools):
        """Test WorkplaceTools.get_org_chart method success."""
        # Mock network analyzer
        mock_analyzer = AsyncMock()
        mock_analyzer.get_org_chart_data.return_value = {"Engineering": ["Manager", "Developer"]}
        workplace_tools.network_analyzer = mock_analyzer

        result = await workplace_tools.get_org_chart(department="Engineering")

        assert "📊" in result
        assert "Engineering" in result
        mock_analyzer.get_org_chart_data.assert_called_once_with("Engineering")

    @pytest.mark.asyncio
    async def test_get_org_chart_method_no_data(self, workplace_tools):
        """Test WorkplaceTools.get_org_chart method with no data."""
        # Mock network analyzer
        mock_analyzer = AsyncMock()
        mock_analyzer.get_org_chart_data.return_value = None
        workplace_tools.network_analyzer = mock_analyzer

        result = await workplace_tools.get_org_chart()

        assert "📊" in result
        assert "No organizational structure found" in result

    @pytest.mark.asyncio
    async def test_get_org_chart_method_failure(self, workplace_tools):
        """Test WorkplaceTools.get_org_chart method failure."""
        with patch.object(workplace_tools, '_get_network_analyzer', side_effect=Exception("Network error")):
            result = await workplace_tools.get_org_chart(department="Engineering")

            assert "❌" in result
            assert "Network error" in result

    @pytest.mark.asyncio
    async def test_export_data_method_csv_success(self, workplace_tools):
        """Test WorkplaceTools.export_data method CSV success."""
        # Mock export manager
        mock_exporter = AsyncMock()
        mock_exporter.export_contacts_csv.return_value = True
        workplace_tools.export_manager = mock_exporter

        result = await workplace_tools.export_data(format="csv", output_path="./test_export")

        assert "💾" in result
        assert "test_export/contacts.csv" in result
        mock_exporter.export_contacts_csv.assert_called_once_with("./test_export/contacts.csv")

    @pytest.mark.asyncio
    async def test_export_data_method_csv_failure(self, workplace_tools):
        """Test WorkplaceTools.export_data method CSV failure."""
        # Mock export manager
        mock_exporter = AsyncMock()
        mock_exporter.export_contacts_csv.return_value = False
        workplace_tools.export_manager = mock_exporter

        result = await workplace_tools.export_data(format="csv")

        assert "❌" in result
        assert "Failed to export data" in result

    @pytest.mark.asyncio
    async def test_export_data_method_unsupported_format(self, workplace_tools):
        """Test WorkplaceTools.export_data method with unsupported format."""
        result = await workplace_tools.export_data(format="xml")

        assert "❌" in result
        assert "Unsupported format: xml" in result

    @pytest.mark.asyncio
    async def test_export_data_method_exception(self, workplace_tools):
        """Test WorkplaceTools.export_data method exception."""
        with patch.object(workplace_tools, '_get_export_manager', side_effect=Exception("Export error")):
            result = await workplace_tools.export_data(format="csv")

            assert "❌" in result
            assert "Export error" in result

    @pytest.mark.asyncio
    async def test_get_network_insights_method_person_specific(self, workplace_tools):
        """Test WorkplaceTools.get_network_insights method for specific person."""
        # Mock network analyzer
        mock_analyzer = Mock()  # Use Mock instead of AsyncMock for better control
        mock_analyzer.build_graph_from_neo4j = AsyncMock()
        mock_analyzer.calculate_centrality_metrics = Mock(return_value={
            "john@test.com": Mock(betweenness_centrality=0.5)
        })
        workplace_tools.network_analyzer = mock_analyzer

        result = await workplace_tools.get_network_insights(person="john@test.com")

        assert "🔍" in result
        assert "john@test.com" in result
        assert "0.500" in result
        mock_analyzer.build_graph_from_neo4j.assert_called_once()
        mock_analyzer.calculate_centrality_metrics.assert_called_once_with("john@test.com")

    @pytest.mark.asyncio
    async def test_get_network_insights_method_general(self, workplace_tools):
        """Test WorkplaceTools.get_network_insights method for general insights."""
        # Mock network analyzer
        mock_analyzer = AsyncMock()
        mock_analyzer.build_graph_from_neo4j.return_value = None
        mock_analyzer.graph = Mock()
        mock_analyzer.graph.number_of_nodes.return_value = 10
        mock_analyzer.graph.number_of_edges.return_value = 25
        workplace_tools.network_analyzer = mock_analyzer

        result = await workplace_tools.get_network_insights()

        assert "🔍" in result
        assert "10 people" in result
        assert "25 connections" in result
        mock_analyzer.build_graph_from_neo4j.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_network_insights_method_person_not_found(self, workplace_tools):
        """Test WorkplaceTools.get_network_insights method when person not found."""
        # Mock network analyzer
        mock_analyzer = Mock()  # Use Mock instead of AsyncMock
        mock_analyzer.build_graph_from_neo4j = AsyncMock()
        mock_analyzer.calculate_centrality_metrics = Mock(return_value={})  # Person not found
        mock_analyzer.graph = Mock()
        mock_analyzer.graph.number_of_nodes.return_value = 5
        mock_analyzer.graph.number_of_edges.return_value = 10
        workplace_tools.network_analyzer = mock_analyzer

        result = await workplace_tools.get_network_insights(person="unknown@test.com")

        assert "🔍" in result
        assert "5 people" in result
        assert "10 connections" in result

    @pytest.mark.asyncio
    async def test_get_network_insights_method_failure(self, workplace_tools):
        """Test WorkplaceTools.get_network_insights method failure."""
        with patch.object(workplace_tools, '_get_network_analyzer', side_effect=Exception("Analyzer error")):
            result = await workplace_tools.get_network_insights()

            assert "❌" in result
            assert "Analyzer error" in result
