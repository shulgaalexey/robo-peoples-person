"""Export manager for workplace social graph data."""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ..database import Interaction, Neo4jManager, Person
from .network_analysis import NetworkAnalyzer

logger = logging.getLogger(__name__)


class ExportManager:
    """Manager for exporting workplace social graph data in various formats."""

    def __init__(self, neo4j_manager: Neo4jManager):
        """Initialize export manager.

        Args:
            neo4j_manager: Neo4j database manager for data access
        """
        self.neo4j_manager = neo4j_manager
        self.network_analyzer = NetworkAnalyzer(neo4j_manager)

    async def export_contacts_csv(
        self,
        output_path: Union[str, Path],
        department: str = None,
        include_personal_notes: bool = False
    ) -> bool:
        """Export contact list to CSV format.

        Args:
            output_path: Path for the output CSV file
            department: Optional department filter
            include_personal_notes: Whether to include personal notes

        Returns:
            bool: True if export successful
        """
        try:
            contacts = []

            async with self.neo4j_manager.session() as session:
                query = "MATCH (p:Person)"
                params = {}

                if department:
                    query += " WHERE p.department = $department"
                    params["department"] = department

                query += " RETURN p ORDER BY p.name"

                result = await session.run(query, **params)
                async for record in result:
                    person_data = record["p"]

                    contact = {
                        'Name': person_data.get('name', ''),
                        'Email': person_data.get('email', ''),
                        'Phone': person_data.get('phone', ''),
                        'Role': person_data.get('role', ''),
                        'Department': person_data.get('department', ''),
                        'Manager': person_data.get('manager', ''),
                        'Expertise Areas': ', '.join(person_data.get('expertise_areas', [])),
                        'Communication Preference': person_data.get('communication_preference', ''),
                        'Timezone': person_data.get('timezone', ''),
                        'Last Interaction': person_data.get('last_interaction', ''),
                        'Interaction Frequency': person_data.get('interaction_frequency', ''),
                    }

                    if include_personal_notes:
                        contact['Notes'] = person_data.get('notes', '')

                    contacts.append(contact)

            # Write to CSV
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                if contacts:
                    fieldnames = contacts[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(contacts)

            logger.info(f"✅ Exported {len(contacts)} contacts to {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export contacts CSV: {e}")
            return False

    async def export_org_chart_json(
        self,
        output_path: Union[str, Path],
        department: str = None
    ) -> bool:
        """Export organizational chart to JSON format.

        Args:
            output_path: Path for the output JSON file
            department: Optional department filter

        Returns:
            bool: True if export successful
        """
        try:
            # Build the graph for analysis
            await self.network_analyzer.build_directed_graph_from_neo4j()

            # Get organizational chart data
            org_chart = await self.network_analyzer.get_org_chart_data()

            # Filter by department if specified
            if department:
                org_chart = self._filter_org_chart_by_department(org_chart, department)

            # Add metadata
            export_data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'export_type': 'organizational_chart',
                    'department_filter': department,
                    'total_people': self._count_people_in_org_chart(org_chart)
                },
                'organizational_chart': org_chart
            }

            # Write to JSON
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, default=str)

            logger.info(f"✅ Exported organizational chart to {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export org chart JSON: {e}")
            return False

    async def export_team_structure_json(
        self,
        output_path: Union[str, Path],
        department: str = None
    ) -> bool:
        """Export team structure with relationships to JSON format.

        Args:
            output_path: Path for the output JSON file
            department: Optional department filter

        Returns:
            bool: True if export successful
        """
        try:
            team_structure = {
                'teams': {},
                'relationships': [],
                'expertise_map': {}
            }

            async with self.neo4j_manager.session() as session:
                # Get all people grouped by department
                people_query = "MATCH (p:Person)"
                params = {}

                if department:
                    people_query += " WHERE p.department = $department"
                    params["department"] = department

                people_query += " RETURN p ORDER BY p.department, p.name"

                result = await session.run(people_query, **params)

                async for record in result:
                    person_data = record["p"]
                    dept = person_data.get('department', 'Unknown')

                    if dept not in team_structure['teams']:
                        team_structure['teams'][dept] = {
                            'members': [],
                            'managers': [],
                            'total_count': 0
                        }

                    member_info = {
                        'name': person_data.get('name', ''),
                        'role': person_data.get('role', ''),
                        'email': person_data.get('email', ''),
                        'expertise_areas': person_data.get('expertise_areas', []),
                        'manager': person_data.get('manager', '')
                    }

                    team_structure['teams'][dept]['members'].append(member_info)
                    team_structure['teams'][dept]['total_count'] += 1

                    # Track managers
                    if person_data.get('manager'):
                        if person_data['manager'] not in team_structure['teams'][dept]['managers']:
                            team_structure['teams'][dept]['managers'].append(person_data['manager'])

                    # Build expertise map
                    for skill in person_data.get('expertise_areas', []):
                        if skill not in team_structure['expertise_map']:
                            team_structure['expertise_map'][skill] = []
                        team_structure['expertise_map'][skill].append(person_data.get('name', ''))

                # Get relationships
                relationships_query = """
                MATCH (from:Person)-[r:WORKS_WITH]->(to:Person)
                """

                if department:
                    relationships_query += " WHERE from.department = $department OR to.department = $department"

                relationships_query += """
                RETURN from.name as from_person,
                       to.name as to_person,
                       r.type as relationship_type,
                       r.context as context,
                       r.strength as strength
                """

                result = await session.run(relationships_query, **params)

                async for record in result:
                    relationship = {
                        'from': record['from_person'],
                        'to': record['to_person'],
                        'type': record['relationship_type'],
                        'context': record['context'],
                        'strength': record['strength']
                    }
                    team_structure['relationships'].append(relationship)

            # Add metadata
            export_data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'export_type': 'team_structure',
                    'department_filter': department,
                    'total_teams': len(team_structure['teams']),
                    'total_relationships': len(team_structure['relationships']),
                    'total_expertise_areas': len(team_structure['expertise_map'])
                },
                'team_structure': team_structure
            }

            # Write to JSON
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, default=str)

            logger.info(f"✅ Exported team structure to {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export team structure JSON: {e}")
            return False

    async def export_network_metrics_csv(
        self,
        output_path: Union[str, Path],
        department: str = None
    ) -> bool:
        """Export network analysis metrics to CSV format.

        Args:
            output_path: Path for the output CSV file
            department: Optional department filter

        Returns:
            bool: True if export successful
        """
        try:
            # Build the graph for analysis
            await self.network_analyzer.build_graph_from_neo4j()

            # Calculate centrality metrics
            all_metrics = self.network_analyzer.calculate_centrality_metrics()

            # Filter by department if specified
            if department:
                filtered_metrics = {}
                for person_name, metrics in all_metrics.items():
                    if self.network_analyzer.graph.nodes[person_name].get('department') == department:
                        filtered_metrics[person_name] = metrics
                all_metrics = filtered_metrics

            # Convert to list of dictionaries for CSV
            metrics_data = []
            for person_name, metrics in all_metrics.items():
                person_data = self.network_analyzer.graph.nodes[person_name]

                row = {
                    'Name': person_name,
                    'Department': person_data.get('department', ''),
                    'Role': person_data.get('role', ''),
                    'Total Connections': metrics.total_connections,
                    'Degree Centrality': round(metrics.degree_centrality, 4),
                    'Betweenness Centrality': round(metrics.betweenness_centrality, 4),
                    'Closeness Centrality': round(metrics.closeness_centrality, 4),
                    'Eigenvector Centrality': round(metrics.eigenvector_centrality, 4),
                    'Expertise Areas': ', '.join(person_data.get('expertise_areas', []))
                }
                metrics_data.append(row)

            # Sort by degree centrality (most connected first)
            metrics_data.sort(key=lambda x: x['Degree Centrality'], reverse=True)

            # Write to CSV
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                if metrics_data:
                    fieldnames = metrics_data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(metrics_data)

            logger.info(f"✅ Exported network metrics for {len(metrics_data)} people to {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export network metrics CSV: {e}")
            return False

    async def export_interactions_csv(
        self,
        output_path: Union[str, Path],
        person_name: str = None,
        days: int = 30
    ) -> bool:
        """Export interaction history to CSV format.

        Args:
            output_path: Path for the output CSV file
            person_name: Optional person name filter
            days: Number of days to look back

        Returns:
            bool: True if export successful
        """
        try:
            interactions = []

            async with self.neo4j_manager.session() as session:
                query = """
                MATCH (i:Interaction)
                WHERE i.date >= datetime() - duration({days: $days})
                """

                params = {"days": days}

                if person_name:
                    query += " AND i.with_person = $person_name"
                    params["person_name"] = person_name

                query += " RETURN i ORDER BY i.date DESC"

                result = await session.run(query, **params)

                async for record in result:
                    interaction_data = record["i"]

                    interaction = {
                        'Date': interaction_data.get('date', ''),
                        'With Person': interaction_data.get('with_person', ''),
                        'Type': interaction_data.get('interaction_type', ''),
                        'Topic': interaction_data.get('topic', ''),
                        'Outcome': interaction_data.get('outcome', ''),
                        'Duration (minutes)': interaction_data.get('duration_minutes', ''),
                        'Project': interaction_data.get('project', ''),
                        'Location': interaction_data.get('location', ''),
                        'Participants': ', '.join(interaction_data.get('participants', [])),
                        'Follow-up Required': interaction_data.get('follow_up_required', False),
                        'Follow-up Date': interaction_data.get('follow_up_date', ''),
                        'Notes': interaction_data.get('notes', '')
                    }

                    interactions.append(interaction)

            # Write to CSV
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                if interactions:
                    fieldnames = interactions[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(interactions)

            logger.info(f"✅ Exported {len(interactions)} interactions to {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export interactions CSV: {e}")
            return False

    def _filter_org_chart_by_department(self, org_chart: Dict[str, Any], department: str) -> Dict[str, Any]:
        """Filter organizational chart by department.

        Args:
            org_chart: Original org chart data
            department: Department to filter by

        Returns:
            Dict[str, Any]: Filtered org chart
        """
        def filter_hierarchy(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            """Recursively filter hierarchy nodes."""
            if node.get('department') == department:
                # Include this node and all its reports
                return node

            # Check if any direct reports are in the target department
            filtered_reports = []
            for report in node.get('direct_reports', []):
                filtered_report = filter_hierarchy(report)
                if filtered_report:
                    filtered_reports.append(filtered_report)

            # If we have filtered reports, include this node as a parent
            if filtered_reports:
                filtered_node = node.copy()
                filtered_node['direct_reports'] = filtered_reports
                return filtered_node

            return None

        filtered_chart = {
            'top_level_managers': [],
            'hierarchy': {}
        }

        for manager, hierarchy in org_chart['hierarchy'].items():
            filtered_hierarchy = filter_hierarchy(hierarchy)
            if filtered_hierarchy:
                filtered_chart['hierarchy'][manager] = filtered_hierarchy
                if manager not in filtered_chart['top_level_managers']:
                    filtered_chart['top_level_managers'].append(manager)

        return filtered_chart

    def _count_people_in_org_chart(self, org_chart: Dict[str, Any]) -> int:
        """Count total people in organizational chart.

        Args:
            org_chart: Org chart data

        Returns:
            int: Total number of people
        """
        def count_in_hierarchy(node: Dict[str, Any]) -> int:
            """Recursively count people in hierarchy."""
            count = 1  # Count this node
            for report in node.get('direct_reports', []):
                count += count_in_hierarchy(report)
            return count

        total_count = 0
        for hierarchy in org_chart['hierarchy'].values():
            total_count += count_in_hierarchy(hierarchy)

        return total_count

    async def export_expertise_directory_json(
        self,
        output_path: Union[str, Path],
        expertise_area: str = None
    ) -> bool:
        """Export expertise directory to JSON format.

        Args:
            output_path: Path for the output JSON file
            expertise_area: Optional expertise area filter

        Returns:
            bool: True if export successful
        """
        try:
            # Build the graph for analysis
            await self.network_analyzer.build_graph_from_neo4j()

            # Get expertise clusters
            expertise_clusters = self.network_analyzer.find_expertise_clusters(expertise_area)

            # Enhanced expertise directory with additional context
            expertise_directory = {}

            for skill, people in expertise_clusters.items():
                expertise_directory[skill] = {
                    'experts': [],
                    'total_count': len(people),
                    'departments': set(),
                    'knowledge_brokers': []
                }

                for person_name in people:
                    person_data = self.network_analyzer.graph.nodes[person_name]

                    expert_info = {
                        'name': person_name,
                        'role': person_data.get('role', ''),
                        'department': person_data.get('department', ''),
                        'email': person_data.get('email', ''),
                        'other_expertise': [
                            e for e in person_data.get('expertise_areas', [])
                            if e != skill
                        ]
                    }

                    expertise_directory[skill]['experts'].append(expert_info)
                    expertise_directory[skill]['departments'].add(person_data.get('department', ''))

                # Convert set to list for JSON serialization
                expertise_directory[skill]['departments'] = list(expertise_directory[skill]['departments'])

                # Find knowledge brokers for this skill
                brokers = self.network_analyzer.find_knowledge_brokers(skill)
                expertise_directory[skill]['knowledge_brokers'] = brokers

            # Add metadata
            export_data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'export_type': 'expertise_directory',
                    'expertise_filter': expertise_area,
                    'total_expertise_areas': len(expertise_directory),
                    'total_experts': sum(cluster['total_count'] for cluster in expertise_directory.values())
                },
                'expertise_directory': expertise_directory
            }

            # Write to JSON
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, default=str)

            logger.info(f"✅ Exported expertise directory to {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to export expertise directory JSON: {e}")
            return False
