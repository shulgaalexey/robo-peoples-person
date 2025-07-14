"""Network analysis engine for workplace social graph insights."""

import logging
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

import networkx as nx
import pandas as pd

from ..database import Neo4jManager, NetworkMetrics, Person

logger = logging.getLogger(__name__)


class NetworkAnalyzer:
    """Workplace network analysis engine using NetworkX."""

    def __init__(self, neo4j_manager: Neo4jManager):
        """Initialize network analyzer.

        Args:
            neo4j_manager: Neo4j database manager for data access
        """
        self.neo4j_manager = neo4j_manager
        self.graph: Optional[nx.Graph] = None
        self.directed_graph: Optional[nx.DiGraph] = None

    async def build_graph_from_neo4j(self, include_interactions: bool = True) -> nx.Graph:
        """Build NetworkX graph from Neo4j workplace data.

        Args:
            include_interactions: Whether to include interaction weights

        Returns:
            nx.Graph: NetworkX graph representation
        """
        graph = nx.Graph()

        async with self.neo4j_manager.session() as session:
            # Get all people and their attributes
            people_query = """
            MATCH (p:Person)
            RETURN p.name as name,
                   p.role as role,
                   p.department as department,
                   p.expertise_areas as expertise_areas,
                   p.manager as manager
            """

            result = await session.run(people_query)
            async for record in result:
                graph.add_node(
                    record["name"],
                    role=record["role"],
                    department=record["department"],
                    expertise_areas=record["expertise_areas"] or [],
                    manager=record["manager"]
                )

            # Get all relationships
            relationships_query = """
            MATCH (from:Person)-[r:WORKS_WITH]->(to:Person)
            RETURN from.name as from_person,
                   to.name as to_person,
                   r.type as relationship_type,
                   r.strength as strength,
                   r.context as context
            """

            result = await session.run(relationships_query)
            async for record in result:
                graph.add_edge(
                    record["from_person"],
                    record["to_person"],
                    relationship_type=record["relationship_type"],
                    strength=record["strength"] or 1.0,
                    context=record["context"]
                )

            # Optionally include interaction weights
            if include_interactions:
                await self._add_interaction_weights(session, graph)

        self.graph = graph
        return graph

    async def build_directed_graph_from_neo4j(self) -> nx.DiGraph:
        """Build directed NetworkX graph for hierarchical analysis.

        Returns:
            nx.DiGraph: Directed graph showing reporting relationships
        """
        directed_graph = nx.DiGraph()

        async with self.neo4j_manager.session() as session:
            # Get all people
            people_query = """
            MATCH (p:Person)
            RETURN p.name as name,
                   p.role as role,
                   p.department as department,
                   p.expertise_areas as expertise_areas,
                   p.manager as manager
            """

            result = await session.run(people_query)
            async for record in result:
                directed_graph.add_node(
                    record["name"],
                    role=record["role"],
                    department=record["department"],
                    expertise_areas=record["expertise_areas"] or [],
                    manager=record["manager"]
                )

            # Get hierarchical relationships (directed)
            hierarchy_query = """
            MATCH (report:Person)-[r:WORKS_WITH {type: 'manager'}]->(manager:Person)
            RETURN report.name as report,
                   manager.name as manager,
                   r.strength as strength
            """

            result = await session.run(hierarchy_query)
            async for record in result:
                directed_graph.add_edge(
                    record["report"],
                    record["manager"],
                    relationship_type="reports_to",
                    strength=record["strength"] or 1.0
                )

        self.directed_graph = directed_graph
        return directed_graph

    async def _add_interaction_weights(self, session, graph: nx.Graph) -> None:
        """Add interaction frequency weights to graph edges."""
        interactions_query = """
        MATCH (i:Interaction)
        RETURN i.with_person as person,
               COUNT(i) as interaction_count
        """

        result = await session.run(interactions_query)
        interaction_weights = {}

        async for record in result:
            person = record["person"]
            count = record["interaction_count"]
            interaction_weights[person] = count

        # Update edge weights based on interaction frequency
        for edge in graph.edges():
            person1, person2 = edge
            weight1 = interaction_weights.get(person1, 0)
            weight2 = interaction_weights.get(person2, 0)
            # Use average interaction frequency as edge weight
            avg_weight = (weight1 + weight2) / 2 if weight1 or weight2 else 1.0
            graph[person1][person2]['interaction_weight'] = avg_weight

    def calculate_centrality_metrics(self, person_name: str = None) -> Dict[str, NetworkMetrics]:
        """Calculate centrality metrics for the network.

        Args:
            person_name: Optional specific person to analyze

        Returns:
            Dict[str, NetworkMetrics]: Centrality metrics by person
        """
        if self.graph is None:
            raise ValueError("Graph not built. Call build_graph_from_neo4j() first.")

        # Handle empty graphs
        if len(self.graph.nodes()) == 0:
            return {}

        # Calculate various centrality measures
        degree_centrality = nx.degree_centrality(self.graph)
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        closeness_centrality = nx.closeness_centrality(self.graph)
        eigenvector_centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)

        # If specific person requested, return only their metrics
        if person_name:
            if person_name not in self.graph:
                raise ValueError(f"Person '{person_name}' not found in graph")

            return {
                person_name: NetworkMetrics(
                    person_name=person_name,
                    degree_centrality=degree_centrality.get(person_name, 0.0),
                    betweenness_centrality=betweenness_centrality.get(person_name, 0.0),
                    closeness_centrality=closeness_centrality.get(person_name, 0.0),
                    eigenvector_centrality=eigenvector_centrality.get(person_name, 0.0),
                    total_connections=self.graph.degree(person_name),
                    graph_size=len(self.graph.nodes())
                )
            }

        # Return metrics for all people
        metrics = {}
        for person in self.graph.nodes():
            metrics[person] = NetworkMetrics(
                person_name=person,
                degree_centrality=degree_centrality.get(person, 0.0),
                betweenness_centrality=betweenness_centrality.get(person, 0.0),
                closeness_centrality=closeness_centrality.get(person, 0.0),
                eigenvector_centrality=eigenvector_centrality.get(person, 0.0),
                total_connections=self.graph.degree(person),
                graph_size=len(self.graph.nodes())
            )

        return metrics

    def find_expertise_clusters(self, expertise_area: str = None) -> Dict[str, List[str]]:
        """Find clusters of people by expertise area.

        Args:
            expertise_area: Optional specific expertise to filter by

        Returns:
            Dict[str, List[str]]: Clusters of people by expertise
        """
        if not self.graph:
            raise ValueError("Graph not built. Call build_graph_from_neo4j() first.")

        expertise_clusters = defaultdict(list)

        for node in self.graph.nodes(data=True):
            person_name = node[0]
            person_data = node[1]
            expertise_areas = person_data.get('expertise_areas', [])

            if expertise_area:
                # Filter by specific expertise
                if any(expertise_area.lower() in skill.lower() for skill in expertise_areas):
                    expertise_clusters[expertise_area].append(person_name)
            else:
                # Group by all expertise areas
                for skill in expertise_areas:
                    expertise_clusters[skill].append(person_name)

        return dict(expertise_clusters)

    def find_collaboration_paths(self, from_person: str, to_person: str) -> List[List[str]]:
        """Find possible collaboration paths between two people.

        Args:
            from_person: Starting person
            to_person: Target person

        Returns:
            List[List[str]]: List of possible paths (each path is a list of names)
        """
        if not self.graph:
            raise ValueError("Graph not built. Call build_graph_from_neo4j() first.")

        if from_person not in self.graph or to_person not in self.graph:
            return []

        try:
            # Find shortest path
            shortest_path = nx.shortest_path(self.graph, from_person, to_person)
            paths = [shortest_path]

            # Find alternative paths (up to 3 total)
            try:
                all_simple_paths = list(nx.all_simple_paths(
                    self.graph, from_person, to_person, cutoff=4
                ))
                # Sort by length and take top 3
                all_simple_paths.sort(key=len)
                paths = all_simple_paths[:3]
            except nx.NetworkXNoPath:
                pass

            return paths

        except nx.NetworkXNoPath:
            return []

    def analyze_department_connectivity(self) -> Dict[str, Dict[str, Any]]:
        """Analyze connectivity within and between departments.

        Returns:
            Dict[str, Dict[str, Any]]: Department connectivity metrics
        """
        if not self.graph:
            raise ValueError("Graph not built. Call build_graph_from_neo4j() first.")

        department_metrics = {}
        departments = defaultdict(list)

        # Group people by department
        for node in self.graph.nodes(data=True):
            person_name = node[0]
            person_data = node[1]
            department = person_data.get('department', 'Unknown')
            departments[department].append(person_name)

        for dept_name, dept_members in departments.items():
            if len(dept_members) < 2:
                continue

            # Create subgraph for department
            dept_subgraph = self.graph.subgraph(dept_members)

            # Calculate internal connectivity
            internal_edges = dept_subgraph.number_of_edges()
            possible_internal_edges = len(dept_members) * (len(dept_members) - 1) / 2
            internal_density = internal_edges / possible_internal_edges if possible_internal_edges > 0 else 0

            # Calculate external connections
            external_connections = 0
            for member in dept_members:
                for neighbor in self.graph.neighbors(member):
                    neighbor_dept = self.graph.nodes[neighbor].get('department', 'Unknown')
                    if neighbor_dept != dept_name:
                        external_connections += 1

            department_metrics[dept_name] = {
                'member_count': len(dept_members),
                'internal_connections': internal_edges,
                'external_connections': external_connections,
                'internal_density': internal_density,
                'avg_external_connections_per_person': external_connections / len(dept_members),
                'members': dept_members
            }

        return department_metrics

    def find_influential_people(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """Find the most influential people in the workplace network.

        Args:
            top_n: Number of top influential people to return

        Returns:
            List[Tuple[str, float]]: List of (person_name, influence_score) tuples
        """
        if not self.graph:
            raise ValueError("Graph not built. Call build_graph_from_neo4j() first.")

        # Calculate combined influence score using multiple centrality measures
        degree_centrality = nx.degree_centrality(self.graph)
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        eigenvector_centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)

        influence_scores = {}
        for person in self.graph.nodes():
            # Weighted combination of centrality measures
            influence_score = (
                0.3 * degree_centrality.get(person, 0) +
                0.4 * betweenness_centrality.get(person, 0) +
                0.3 * eigenvector_centrality.get(person, 0)
            )
            influence_scores[person] = influence_score

        # Sort by influence score and return top N
        sorted_influential = sorted(
            influence_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_influential[:top_n]

    def find_knowledge_brokers(self, expertise_area: str) -> List[str]:
        """Find people who bridge different expertise areas.

        Args:
            expertise_area: The expertise area to analyze

        Returns:
            List[str]: List of knowledge broker names
        """
        if not self.graph:
            raise ValueError("Graph not built. Call build_graph_from_neo4j() first.")

        expertise_specialists = []
        for node in self.graph.nodes(data=True):
            person_name = node[0]
            person_data = node[1]
            expertise_areas = person_data.get('expertise_areas', [])

            if any(expertise_area.lower() in skill.lower() for skill in expertise_areas):
                expertise_specialists.append(person_name)

        if not expertise_specialists:
            return []

        # Find people who connect expertise specialists to others
        brokers = []
        betweenness_centrality = nx.betweenness_centrality(self.graph)

        for person in self.graph.nodes():
            if person in expertise_specialists:
                continue

            # Check if this person bridges to expertise specialists
            specialist_connections = 0
            for neighbor in self.graph.neighbors(person):
                if neighbor in expertise_specialists:
                    specialist_connections += 1

            # If connected to multiple specialists and has high betweenness, they're a broker
            if specialist_connections >= 2 and betweenness_centrality.get(person, 0) > 0.1:
                brokers.append(person)

        # Sort by betweenness centrality
        brokers.sort(key=lambda x: betweenness_centrality.get(x, 0), reverse=True)

        return brokers[:5]  # Return top 5 brokers

    async def get_org_chart_data(self) -> Dict[str, Any]:
        """Generate organizational chart data structure.

        Returns:
            Dict[str, Any]: Hierarchical organization structure
        """
        if not self.directed_graph:
            await self.build_directed_graph_from_neo4j()

        # Find all managers (nodes with incoming "reports_to" edges)
        managers = set()
        reports = set()

        for edge in self.directed_graph.edges():
            report, manager = edge
            managers.add(manager)
            reports.add(report)

        # Find top-level managers (managers who don't report to anyone)
        top_level_managers = managers - reports

        org_chart = {
            'top_level_managers': list(top_level_managers),
            'hierarchy': {}
        }

        def build_hierarchy(manager: str) -> Dict[str, Any]:
            """Recursively build hierarchy for a manager."""
            direct_reports = []
            for edge in self.directed_graph.edges():
                report, mgr = edge
                if mgr == manager:
                    direct_reports.append(report)

            manager_data = {
                'name': manager,
                'role': self.directed_graph.nodes[manager].get('role', ''),
                'department': self.directed_graph.nodes[manager].get('department', ''),
                'direct_reports': []
            }

            for report in direct_reports:
                # Recursively build hierarchy for each direct report
                if report in managers:  # If this report is also a manager
                    manager_data['direct_reports'].append(build_hierarchy(report))
                else:
                    # Leaf node (individual contributor)
                    manager_data['direct_reports'].append({
                        'name': report,
                        'role': self.directed_graph.nodes[report].get('role', ''),
                        'department': self.directed_graph.nodes[report].get('department', ''),
                        'direct_reports': []
                    })

            return manager_data

        # Build hierarchy for each top-level manager
        for manager in top_level_managers:
            org_chart['hierarchy'][manager] = build_hierarchy(manager)

        return org_chart
