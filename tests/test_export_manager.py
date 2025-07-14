"""Tests for export manager functionality."""

from unittest.mock import AsyncMock, Mock, mock_open, patch

import pytest

from src.analysis.export_manager import ExportManager
from src.config.settings import Settings
from src.database.models import Person


class TestExportManager:
    """Test cases for ExportManager."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings()

    @pytest.fixture
    def export_manager(self, settings):
        """Create ExportManager instance."""
        mock_neo4j = Mock()
        return ExportManager(mock_neo4j)

    def test_init(self, export_manager):
        """Test ExportManager initialization."""
        assert export_manager.neo4j_manager is not None
        assert export_manager.network_analyzer is not None

    @pytest.mark.asyncio
    async def test_export_contacts_csv(self, export_manager):
        """Test exporting contacts to CSV."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                result = await export_manager.export_contacts_csv('test.csv')

                assert result is True

    @pytest.mark.asyncio
    async def test_export_org_chart_json(self, export_manager):
        """Test exporting org chart to JSON."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                result = await export_manager.export_org_chart_json('test.json')

                assert result is True

    @pytest.mark.asyncio
    async def test_export_team_structure_json(self, export_manager):
        """Test exporting team structure to JSON."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                result = await export_manager.export_team_structure_json('test.json')

                assert result is True

    @pytest.mark.asyncio
    async def test_export_network_metrics_csv(self, export_manager):
        """Test exporting network metrics to CSV."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.network_analyzer, 'build_graph_from_neo4j'):
                with patch.object(export_manager.network_analyzer, 'calculate_centrality_metrics', return_value={}):

                    result = await export_manager.export_network_metrics_csv('test.csv')

                    assert result is True

    @pytest.mark.asyncio
    async def test_export_interactions_csv(self, export_manager):
        """Test exporting interactions to CSV."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                result = await export_manager.export_interactions_csv('test.csv')

                assert result is True

    @pytest.mark.asyncio
    async def test_export_expertise_directory_json(self, export_manager):
        """Test exporting expertise directory to JSON."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                # Mock network analyzer and its methods properly
                export_manager.network_analyzer = Mock()
                export_manager.network_analyzer.build_graph_from_neo4j = AsyncMock()
                export_manager.network_analyzer.find_expertise_clusters = Mock(return_value={'Python': ['John Doe']})
                export_manager.network_analyzer.graph = Mock()
                export_manager.network_analyzer.graph.nodes = {'John Doe': {'role': 'Developer', 'department': 'Engineering', 'email': 'john@test.com'}}

                result = await export_manager.export_expertise_directory_json('test.json')

        assert result is True

    @pytest.mark.asyncio
    async def test_export_contacts_csv_with_department_filter(self, export_manager):
        """Test exporting contacts to CSV with department filter."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                result = await export_manager.export_contacts_csv('test.csv', department='Engineering')

                assert result is True

    @pytest.mark.asyncio
    async def test_export_contacts_csv_with_personal_notes(self, export_manager):
        """Test exporting contacts to CSV with personal notes."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = [
                    {'p': {'name': 'John Doe', 'email': 'john@test.com', 'notes': 'Great collaborator'}}
                ]

                result = await export_manager.export_contacts_csv('test.csv', include_personal_notes=True)

        assert result is True

    @pytest.mark.asyncio
    async def test_export_contacts_csv_failure(self, export_manager):
        """Test export contacts CSV with failure scenario."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session.side_effect = Exception("Database error")

                result = await export_manager.export_contacts_csv('test.csv')

                assert result is False

    @pytest.mark.asyncio
    async def test_export_org_chart_json_with_department_filter(self, export_manager):
        """Test exporting org chart to JSON with department filter."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                # Mock network analyzer and its async methods properly
                export_manager.network_analyzer = Mock()
                export_manager.network_analyzer.build_directed_graph_from_neo4j = AsyncMock()
                mock_org_chart = {
                    'top_level_managers': ['John Smith'],
                    'hierarchy': {
                        'John Smith': {
                            'name': 'John Smith',
                            'department': 'Engineering',
                            'direct_reports': []
                        }
                    }
                }
                export_manager.network_analyzer.get_org_chart_data = AsyncMock(return_value=mock_org_chart)

                with patch.object(export_manager, '_filter_org_chart_by_department') as mock_filter:
                    mock_filter.return_value = mock_org_chart

                    result = await export_manager.export_org_chart_json('test.json', department='Engineering')

                    assert result is True
                    mock_filter.assert_called_once()

    @pytest.mark.asyncio
    async def test_export_org_chart_json_failure(self, export_manager):
        """Test export org chart JSON with failure scenario."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session.side_effect = Exception("Database error")

                result = await export_manager.export_org_chart_json('test.json')

                assert result is False

    @pytest.mark.asyncio
    async def test_export_team_structure_json_with_department_filter(self, export_manager):
        """Test exporting team structure to JSON with department filter."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                result = await export_manager.export_team_structure_json('test.json', department='Engineering')

                assert result is True

    @pytest.mark.asyncio
    async def test_export_team_structure_json_failure(self, export_manager):
        """Test export team structure JSON with failure scenario."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session.side_effect = Exception("Database error")

                result = await export_manager.export_team_structure_json('test.json')

                assert result is False

    @pytest.mark.asyncio
    async def test_export_network_metrics_csv_failure(self, export_manager):
        """Test export network metrics CSV with failure scenario."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.network_analyzer, 'build_graph_from_neo4j'):
                with patch.object(export_manager.network_analyzer, 'calculate_centrality_metrics') as mock_metrics:
                    mock_metrics.side_effect = Exception("Network error")

                    result = await export_manager.export_network_metrics_csv('test.csv')

                    assert result is False

    @pytest.mark.asyncio
    async def test_export_interactions_csv_with_person_filter(self, export_manager):
        """Test exporting interactions to CSV with person filter."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                result = await export_manager.export_interactions_csv('test.csv', person_name='John Doe', days=7)

        assert result is True

    @pytest.mark.asyncio
    async def test_export_interactions_csv_failure(self, export_manager):
        """Test export interactions CSV with failure scenario."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session.side_effect = Exception("Database error")

                result = await export_manager.export_interactions_csv('test.csv')

                assert result is False

    @pytest.mark.asyncio
    async def test_export_expertise_directory_json_failure(self, export_manager):
        """Test export expertise directory JSON with failure scenario."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session.side_effect = Exception("Database error")

                result = await export_manager.export_expertise_directory_json('test.json')

                assert result is False

    def test_filter_org_chart_by_department(self, export_manager):
        """Test filtering org chart by department."""
        org_chart = {
            'top_level_managers': ['John Smith'],
            'hierarchy': {
                'John Smith': {
                    'name': 'John Smith',
                    'department': 'Engineering',
                    'direct_reports': [
                        {
                            'name': 'Jane Doe',
                            'department': 'Engineering',
                            'direct_reports': []
                        },
                        {
                            'name': 'Bob Wilson',
                            'department': 'Marketing',
                            'direct_reports': []
                        }
                    ]
                }
            }
        }

        result = export_manager._filter_org_chart_by_department(org_chart, 'Engineering')

        assert 'top_level_managers' in result
        assert 'hierarchy' in result

    def test_filter_org_chart_by_department_no_match(self, export_manager):
        """Test filtering org chart by department with no matches."""
        org_chart = {
            'top_level_managers': ['John Smith'],
            'hierarchy': {
                'John Smith': {
                    'name': 'John Smith',
                    'department': 'Engineering',
                    'direct_reports': [
                        {
                            'name': 'Bob Wilson',
                            'department': 'Marketing',
                            'direct_reports': []
                        }
                    ]
                }
            }
        }

        result = export_manager._filter_org_chart_by_department(org_chart, 'Finance')

        assert 'top_level_managers' in result
        assert 'hierarchy' in result

    def test_count_people_in_org_chart(self, export_manager):
        """Test counting people in org chart."""
        org_chart = {
            'top_level_managers': ['John Smith'],
            'hierarchy': {
                'John Smith': {
                    'name': 'John Smith',
                    'direct_reports': [
                        {
                            'name': 'Jane Doe',
                            'direct_reports': []
                        },
                        {
                            'name': 'Bob Wilson',
                            'direct_reports': [
                                {
                                    'name': 'Alice Brown',
                                    'direct_reports': []
                                }
                            ]
                        }
                    ]
                }
            }
        }

        result = export_manager._count_people_in_org_chart(org_chart)

        assert result == 4  # John, Jane, Bob, Alice

    def test_count_people_in_empty_org_chart(self, export_manager):
        """Test counting people in empty org chart."""
        org_chart = {
            'top_level_managers': ['John Smith'],
            'hierarchy': {
                'John Smith': {
                    'name': 'John Smith',
                    'direct_reports': []
                }
            }
        }

        result = export_manager._count_people_in_org_chart(org_chart)

        assert result == 1  # Just John

    @pytest.mark.asyncio
    async def test_export_team_structure_json_with_skills_and_relationships(self, export_manager):
        """Test exporting team structure to JSON with skills and relationships."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                # Mock people data with skills and managers
                people_result = AsyncMock()
                people_result.__aiter__.return_value = [
                    {'p': {
                        'name': 'John Doe',
                        'email': 'john@test.com',
                        'department': 'Engineering',
                        'role': 'Developer',
                        'expertise_areas': ['Python', 'AI'],
                        'manager': 'Jane Smith'
                    }},
                    {'p': {
                        'name': 'Jane Smith',
                        'email': 'jane@test.com',
                        'department': 'Engineering',
                        'role': 'Manager',
                        'expertise_areas': ['Leadership'],
                        'manager': None
                    }}
                ]

                # Mock relationships data
                relationships_result = AsyncMock()
                relationships_result.__aiter__.return_value = [
                    {
                        'from_person': 'John Doe',
                        'to_person': 'Jane Smith',
                        'relationship_type': 'reports_to',
                        'context': 'direct_report',
                        'strength': 0.9
                    }
                ]

                mock_session_instance.run.side_effect = [people_result, relationships_result]

                result = await export_manager.export_team_structure_json('test.json')

        assert result is True

    @pytest.mark.asyncio
    async def test_export_network_metrics_csv_with_department_filter(self, export_manager):
        """Test exporting network metrics to CSV with department filter."""
        with patch('builtins.open', mock_open()) as mock_file:
            # Mock network analyzer methods
            mock_centrality_metrics = {
                'John Doe': Mock(
                    total_connections=5,
                    degree_centrality=0.8,
                    betweenness_centrality=0.6,
                    closeness_centrality=0.7,
                    eigenvector_centrality=0.5
                ),
                'Jane Smith': Mock(
                    total_connections=3,
                    degree_centrality=0.6,
                    betweenness_centrality=0.4,
                    closeness_centrality=0.5,
                    eigenvector_centrality=0.3
                )
            }

            # Mock graph with nodes
            mock_graph = Mock()
            mock_graph.nodes = {
                'John Doe': {'department': 'Engineering', 'role': 'Developer', 'expertise_areas': ['Python']},
                'Jane Smith': {'department': 'Marketing', 'role': 'Manager', 'expertise_areas': ['Marketing']}
            }

            with patch.object(export_manager.network_analyzer, 'build_graph_from_neo4j'):
                with patch.object(export_manager.network_analyzer, 'calculate_centrality_metrics', return_value=mock_centrality_metrics):
                    export_manager.network_analyzer.graph = mock_graph

                    result = await export_manager.export_network_metrics_csv('test.csv', department='Engineering')

                    assert result is True

    @pytest.mark.asyncio
    async def test_export_interactions_csv_with_all_fields(self, export_manager):
        """Test exporting interactions to CSV with all possible fields."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = [
                    {'i': {
                        'date': '2023-01-01',
                        'with_person': 'Jane Doe',
                        'interaction_type': 'meeting',
                        'topic': 'Project planning',
                        'outcome': 'Approved',
                        'duration_minutes': 60,
                        'project': 'Alpha',
                        'location': 'Conference Room A',
                        'participants': ['John', 'Jane', 'Bob'],
                        'follow_up_required': True,
                        'follow_up_date': '2023-01-05',
                        'notes': 'Important discussion'
                    }}
                ]

                result = await export_manager.export_interactions_csv('test.csv')

        assert result is True

    @pytest.mark.asyncio
    async def test_export_expertise_directory_json_with_full_data(self, export_manager):
        """Test exporting expertise directory to JSON with full person data."""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch.object(export_manager.neo4j_manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_result = AsyncMock()
                mock_session_instance.run.return_value = mock_result
                mock_result.__aiter__.return_value = []

                # Mock network analyzer and its methods with comprehensive data
                export_manager.network_analyzer = Mock()
                export_manager.network_analyzer.build_graph_from_neo4j = AsyncMock()
                export_manager.network_analyzer.find_expertise_clusters = Mock(return_value={
                    'Python': ['John Doe'],
                    'AI': ['John Doe', 'Jane Smith'],
                    'Leadership': ['Jane Smith']
                })
                export_manager.network_analyzer.graph = Mock()
                export_manager.network_analyzer.graph.nodes = {
                    'John Doe': {
                        'role': 'Developer',
                        'department': 'Engineering',
                        'email': 'john@test.com',
                        'expertise_areas': ['Python', 'AI']
                    },
                    'Jane Smith': {
                        'role': 'Manager',
                        'department': 'Engineering',
                        'email': 'jane@test.com',
                        'expertise_areas': ['AI', 'Leadership']
                    }
                }

                result = await export_manager.export_expertise_directory_json('test.json')

        assert result is True

    def test_filter_org_chart_by_department_with_nested_reports(self, export_manager):
        """Test filtering org chart by department with nested direct reports."""
        org_chart = {
            'top_level_managers': ['CEO'],
            'hierarchy': {
                'CEO': {
                    'name': 'CEO',
                    'department': 'Executive',
                    'direct_reports': [
                        {
                            'name': 'Engineering Manager',
                            'department': 'Engineering',
                            'direct_reports': [
                                {
                                    'name': 'Senior Developer',
                                    'department': 'Engineering',
                                    'direct_reports': []
                                },
                                {
                                    'name': 'Junior Developer',
                                    'department': 'Engineering',
                                    'direct_reports': []
                                }
                            ]
                        },
                        {
                            'name': 'Marketing Manager',
                            'department': 'Marketing',
                            'direct_reports': [
                                {
                                    'name': 'Marketing Specialist',
                                    'department': 'Marketing',
                                    'direct_reports': []
                                }
                            ]
                        }
                    ]
                }
            }
        }

        result = export_manager._filter_org_chart_by_department(org_chart, 'Engineering')

        assert 'top_level_managers' in result
        assert 'hierarchy' in result
        # Should include nodes that have Engineering reports even if they're not Engineering themselves
        assert len(result['hierarchy']) > 0

    def test_filter_org_chart_by_department_deeply_nested(self, export_manager):
        """Test filtering org chart with deeply nested structure."""
        org_chart = {
            'top_level_managers': ['Level1'],
            'hierarchy': {
                'Level1': {
                    'name': 'Level1',
                    'department': 'Management',
                    'direct_reports': [
                        {
                            'name': 'Level2',
                            'department': 'Management',
                            'direct_reports': [
                                {
                                    'name': 'Level3',
                                    'department': 'Engineering',
                                    'direct_reports': [
                                        {
                                            'name': 'Level4',
                                            'department': 'Engineering',
                                            'direct_reports': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }

        result = export_manager._filter_org_chart_by_department(org_chart, 'Engineering')

        assert 'top_level_managers' in result
        assert 'hierarchy' in result

    def test_count_people_in_complex_org_chart(self, export_manager):
        """Test counting people in a complex org chart structure."""
        org_chart = {
            'top_level_managers': ['CEO', 'CTO'],
            'hierarchy': {
                'CEO': {
                    'name': 'CEO',
                    'direct_reports': [
                        {
                            'name': 'VP Sales',
                            'direct_reports': [
                                {'name': 'Sales Manager 1', 'direct_reports': []},
                                {'name': 'Sales Manager 2', 'direct_reports': []}
                            ]
                        }
                    ]
                },
                'CTO': {
                    'name': 'CTO',
                    'direct_reports': [
                        {
                            'name': 'Engineering Manager',
                            'direct_reports': [
                                {'name': 'Developer 1', 'direct_reports': []},
                                {'name': 'Developer 2', 'direct_reports': []},
                                {'name': 'Developer 3', 'direct_reports': []}
                            ]
                        }
                    ]
                }
            }
        }

        result = export_manager._count_people_in_org_chart(org_chart)

        assert result == 9  # CEO, CTO, VP Sales, 2 Sales Managers, Eng Manager, 3 Developers
