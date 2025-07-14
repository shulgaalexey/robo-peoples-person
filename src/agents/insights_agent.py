"""Specialized insights agent for advanced network analysis."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from ..analysis.network_analysis import NetworkAnalyzer
from ..config.settings import Settings
from ..database.neo4j_manager import Neo4jManager

logger = logging.getLogger(__name__)


class InsightsAgent:
    """Specialized agent for generating workplace network insights."""

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the insights agent.

        Args:
            settings: Optional settings instance
        """
        self.settings = settings or Settings()
        self.neo4j_manager = Neo4jManager(self.settings)
        self.network_analyzer = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.neo4j_manager.connect()
        self.network_analyzer = NetworkAnalyzer(self.neo4j_manager)
        await self.network_analyzer.build_graph_from_neo4j()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.neo4j_manager.close()

    async def initialize(self):
        """Initialize the insights agent."""
        await self.neo4j_manager.connect()
        self.network_analyzer = NetworkAnalyzer(self.neo4j_manager)
        await self.network_analyzer.build_graph_from_neo4j()
        logger.info("Insights agent initialized successfully")

    async def close(self):
        """Close database connections."""
        await self.neo4j_manager.close()

    async def generate_daily_insights(self) -> str:
        """Generate daily network insights report.

        Returns:
            str: Formatted daily insights report
        """
        try:
            await self._ensure_network_loaded()

            insights = []
            insights.append("📊 **Daily Workplace Network Insights**")
            insights.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            insights.append("")

            # Network overview
            node_count = len(self.network_analyzer.graph.nodes())
            edge_count = len(self.network_analyzer.graph.edges())
            density = self.network_analyzer.calculate_network_density()

            insights.append("🌐 **Network Overview:**")
            insights.append(f"• Total people: {node_count}")
            insights.append(f"• Total connections: {edge_count}")
            insights.append(f"• Network density: {density:.1%}")
            insights.append("")

            # Top influencers
            influential_people = self.network_analyzer.find_influential_people(top_n=3)
            insights.append("🌟 **Today's Most Influential People:**")
            for i, (person, score) in enumerate(influential_people, 1):
                insights.append(f"{i}. {person} (influence: {score:.3f})")
            insights.append("")

            # Department connectivity
            dept_stats = self.network_analyzer.analyze_department_connectivity()
            if dept_stats:
                most_connected = max(dept_stats.items(), key=lambda x: x[1]["internal_density"])
                insights.append("🏢 **Department Spotlight:**")
                insights.append(f"Most cohesive team: {most_connected[0]}")
                insights.append(f"Team cohesion: {most_connected[1]['internal_density']:.1%}")
                insights.append("")

            # Network health indicators
            health_score = await self._calculate_network_health()
            insights.append("💚 **Network Health Score:**")
            insights.append(f"Overall health: {health_score:.1%}")
            insights.append("")

            # Recommendations
            recommendations = await self._generate_recommendations()
            insights.append("💡 **Recommendations:**")
            for rec in recommendations:
                insights.append(f"• {rec}")

            return "\n".join(insights)

        except Exception as e:
            logger.error(f"Error generating daily insights: {e}")
            return f"❌ Failed to generate daily insights: {str(e)}"

    async def analyze_collaboration_patterns(self, days_back: int = 30) -> str:
        """Analyze collaboration patterns over time.

        Args:
            days_back: Number of days to analyze

        Returns:
            str: Collaboration analysis report
        """
        try:
            await self._ensure_network_loaded()

            insights = []
            insights.append(f"🤝 **Collaboration Patterns Analysis ({days_back} days)**")
            insights.append("")

            # Get recent interactions
            since_date = datetime.now() - timedelta(days=days_back)
            recent_interactions = await self.neo4j_manager.get_interactions_since(since_date)

            insights.append(f"📈 **Activity Summary:**")
            insights.append(f"• Total interactions: {len(recent_interactions)}")
            insights.append(f"• Average per day: {len(recent_interactions) / days_back:.1f}")
            insights.append("")

            # Most active collaborators
            interaction_counts = {}
            for interaction in recent_interactions:
                person1 = interaction.person1_email
                person2 = interaction.person2_email
                interaction_counts[person1] = interaction_counts.get(person1, 0) + 1
                interaction_counts[person2] = interaction_counts.get(person2, 0) + 1

            if interaction_counts:
                top_collaborators = sorted(interaction_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                insights.append("⭐ **Most Active Collaborators:**")
                for email, count in top_collaborators:
                    person = await self.neo4j_manager.get_person_by_email(email)
                    name = person.name if person else email.split('@')[0]
                    insights.append(f"• {name}: {count} interactions")
                insights.append("")

            # Cross-department collaboration
            cross_dept_interactions = await self._analyze_cross_department_collaboration(recent_interactions)
            if cross_dept_interactions:
                insights.append("🌉 **Cross-Department Collaboration:**")
                for (dept1, dept2), count in cross_dept_interactions.items():
                    insights.append(f"• {dept1} ↔ {dept2}: {count} interactions")
                insights.append("")

            # Collaboration trends
            trends = await self._analyze_collaboration_trends(recent_interactions)
            insights.append("📊 **Trends:**")
            for trend in trends:
                insights.append(f"• {trend}")

            return "\n".join(insights)

        except Exception as e:
            logger.error(f"Error analyzing collaboration patterns: {e}")
            return f"❌ Failed to analyze collaboration patterns: {str(e)}"

    async def identify_silos(self) -> str:
        """Identify organizational silos and isolation risks.

        Returns:
            str: Silo analysis report
        """
        try:
            await self._ensure_network_loaded()

            insights = []
            insights.append("🏗️ **Organizational Silo Analysis**")
            insights.append("")

            # Find disconnected components
            components = list(self.network_analyzer.find_communities())
            insights.append(f"🔍 **Network Structure:**")
            insights.append(f"• Total communities: {len(components)}")

            if len(components) > 1:
                insights.append(f"• Warning: {len(components) - 1} isolated groups detected")

                for i, component in enumerate(components, 1):
                    if len(component) > 1:
                        insights.append(f"• Group {i}: {len(component)} people")
                insights.append("")

            # Department isolation analysis
            dept_stats = self.network_analyzer.analyze_department_connectivity()
            isolated_depts = []
            well_connected_depts = []

            for dept, stats in dept_stats.items():
                external_ratio = stats["external_connections"] / max(stats["member_count"], 1)
                if external_ratio < 0.5:  # Less than 0.5 external connections per person
                    isolated_depts.append((dept, external_ratio))
                elif external_ratio > 2.0:  # More than 2 external connections per person
                    well_connected_depts.append((dept, external_ratio))

            if isolated_depts:
                insights.append("🚨 **Potentially Isolated Departments:**")
                for dept, ratio in sorted(isolated_depts, key=lambda x: x[1]):
                    insights.append(f"• {dept}: {ratio:.1f} external connections per person")
                insights.append("")

            if well_connected_depts:
                insights.append("🌟 **Well-Connected Departments:**")
                for dept, ratio in sorted(well_connected_depts, key=lambda x: x[1], reverse=True):
                    insights.append(f"• {dept}: {ratio:.1f} external connections per person")
                insights.append("")

            # Bridge recommendations
            bridges = self.network_analyzer.find_bridge_people(top_n=3)
            if bridges:
                insights.append("🌉 **Key Bridge People (critical connectors):**")
                for person, score in bridges:
                    insights.append(f"• {person}: {score:.3f} bridge score")
                insights.append("")
                insights.append("💡 **Recommendation:** Ensure these bridge people have backup connections")

            # Suggestions for reducing silos
            suggestions = await self._generate_silo_reduction_suggestions(isolated_depts)
            if suggestions:
                insights.append("🔧 **Silo Reduction Suggestions:**")
                for suggestion in suggestions:
                    insights.append(f"• {suggestion}")

            return "\n".join(insights)

        except Exception as e:
            logger.error(f"Error identifying silos: {e}")
            return f"❌ Failed to identify silos: {str(e)}"

    async def recommend_connections(self, person_email: str, limit: int = 5) -> str:
        """Recommend new connections for a specific person.

        Args:
            person_email: Email of the person to make recommendations for
            limit: Maximum number of recommendations

        Returns:
            str: Connection recommendations
        """
        try:
            await self._ensure_network_loaded()

            person = await self.neo4j_manager.get_person_by_email(person_email)
            if not person:
                return f"❌ Person with email {person_email} not found"

            insights = []
            insights.append(f"🤝 **Connection Recommendations for {person.name}**")
            insights.append("")

            # Get current connections
            current_connections = await self.neo4j_manager.get_person_relationships(person_email)
            connected_emails = {rel.person2_email for rel in current_connections}
            connected_emails.add(person_email)  # Don't recommend self

            # Find potential connections based on different criteria
            recommendations = []

            # 1. Same department but not connected
            dept_colleagues = await self.neo4j_manager.find_people_by_department(person.department)
            for colleague in dept_colleagues:
                if colleague.email not in connected_emails and len(recommendations) < limit:
                    recommendations.append({
                        "person": colleague,
                        "reason": f"Same department ({person.department})",
                        "priority": 3
                    })

            # 2. Similar skills
            if person.skills:
                for skill in person.skills:
                    skill_experts = await self.neo4j_manager.find_experts(skill, limit=3)
                    for expert in skill_experts:
                        if expert.email not in connected_emails and len(recommendations) < limit:
                            recommendations.append({
                                "person": expert,
                                "reason": f"Shared expertise in {skill}",
                                "priority": 2
                            })

            # 3. Bridge connections (friends of friends)
            for connection in current_connections:
                if len(recommendations) >= limit:
                    break
                second_degree = await self.neo4j_manager.get_person_relationships(connection.person2_email)
                for second_rel in second_degree:
                    if second_rel.person2_email not in connected_emails and len(recommendations) < limit:
                        bridge_person = await self.neo4j_manager.get_person_by_email(connection.person2_email)
                        potential_connection = await self.neo4j_manager.get_person_by_email(second_rel.person2_email)
                        if bridge_person and potential_connection:
                            recommendations.append({
                                "person": potential_connection,
                                "reason": f"Connected through {bridge_person.name}",
                                "priority": 1
                            })

            # Sort by priority and remove duplicates
            seen_emails = set()
            unique_recommendations = []
            for rec in sorted(recommendations, key=lambda x: -x["priority"]):
                if rec["person"].email not in seen_emails:
                    unique_recommendations.append(rec)
                    seen_emails.add(rec["person"].email)
                    if len(unique_recommendations) >= limit:
                        break

            if unique_recommendations:
                insights.append("💡 **Recommended Connections:**")
                for i, rec in enumerate(unique_recommendations, 1):
                    p = rec["person"]
                    insights.append(f"{i}. **{p.name}** ({p.department})")
                    insights.append(f"   Role: {p.role}")
                    insights.append(f"   Reason: {rec['reason']}")
                    if p.skills:
                        insights.append(f"   Skills: {', '.join(p.skills[:3])}")
                    insights.append("")
            else:
                insights.append("🤔 No new connection recommendations found at this time.")
                insights.append("Consider expanding your network by attending cross-team meetings!")

            return "\n".join(insights)

        except Exception as e:
            logger.error(f"Error recommending connections: {e}")
            return f"❌ Failed to recommend connections: {str(e)}"

    async def _ensure_network_loaded(self):
        """Ensure the network analyzer has current data."""
        if not self.network_analyzer:
            self.network_analyzer = NetworkAnalyzer(self.neo4j_manager)
        await self.network_analyzer.build_graph_from_neo4j()

    async def _calculate_network_health(self) -> float:
        """Calculate overall network health score."""
        try:
            density = self.network_analyzer.calculate_network_density()
            dept_stats = self.network_analyzer.analyze_department_connectivity()

            # Health factors
            density_score = min(density * 10, 1.0)  # Ideal density around 0.1

            # Department connectivity score
            if dept_stats:
                avg_external_ratio = sum(
                    stats["external_connections"] / max(stats["member_count"], 1)
                    for stats in dept_stats.values()
                ) / len(dept_stats)
                connectivity_score = min(avg_external_ratio / 2.0, 1.0)  # Ideal ratio around 2.0
            else:
                connectivity_score = 0.0

            # Overall health (weighted average)
            health_score = (density_score * 0.6) + (connectivity_score * 0.4)
            return health_score

        except Exception as e:
            logger.error(f"Error calculating network health: {e}")
            return 0.0

    async def _generate_recommendations(self) -> List[str]:
        """Generate actionable network recommendations."""
        recommendations = []

        try:
            # Analyze current state
            density = self.network_analyzer.calculate_network_density()
            dept_stats = self.network_analyzer.analyze_department_connectivity()

            # Density recommendations
            if density < 0.05:
                recommendations.append("Consider organizing cross-team social events to increase connections")
            elif density > 0.2:
                recommendations.append("Network is highly connected - focus on quality over quantity in relationships")

            # Department-specific recommendations
            if dept_stats:
                isolated_depts = [
                    dept for dept, stats in dept_stats.items()
                    if stats["external_connections"] / max(stats["member_count"], 1) < 0.5
                ]
                if isolated_depts:
                    recommendations.append(f"Encourage {', '.join(isolated_depts[:2])} to participate in cross-team projects")

            # Bridge people recommendations
            bridges = self.network_analyzer.find_bridge_people(top_n=1)
            if bridges:
                recommendations.append(f"Ensure {bridges[0][0]} has adequate support as a key connector")

            if not recommendations:
                recommendations.append("Network appears healthy - maintain current collaboration patterns")

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Unable to generate specific recommendations at this time")

        return recommendations

    async def _analyze_cross_department_collaboration(self, interactions) -> Dict[Tuple[str, str], int]:
        """Analyze cross-department collaboration from interactions."""
        cross_dept = {}

        for interaction in interactions:
            person1 = await self.neo4j_manager.get_person_by_email(interaction.person1_email)
            person2 = await self.neo4j_manager.get_person_by_email(interaction.person2_email)

            if person1 and person2 and person1.department != person2.department:
                depts = tuple(sorted([person1.department, person2.department]))
                cross_dept[depts] = cross_dept.get(depts, 0) + 1

        return dict(sorted(cross_dept.items(), key=lambda x: x[1], reverse=True)[:5])

    async def _analyze_collaboration_trends(self, interactions) -> List[str]:
        """Analyze trends in collaboration patterns."""
        trends = []

        try:
            if not interactions:
                trends.append("No recent interactions to analyze")
                return trends

            # Interaction types analysis
            type_counts = {}
            for interaction in interactions:
                type_counts[interaction.interaction_type] = type_counts.get(interaction.interaction_type, 0) + 1

            if type_counts:
                most_common = max(type_counts.items(), key=lambda x: x[1])
                trends.append(f"Most common interaction type: {most_common[0]} ({most_common[1]} occurrences)")

            # Time-based patterns could be added here
            trends.append(f"Average interaction frequency: {len(interactions) / 30:.1f} per day")

        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            trends.append("Unable to analyze trends at this time")

        return trends

    async def _generate_silo_reduction_suggestions(self, isolated_depts) -> List[str]:
        """Generate suggestions for reducing departmental silos."""
        suggestions = []

        if not isolated_depts:
            return ["No significant silos detected - good cross-department connectivity!"]

        for dept, ratio in isolated_depts:
            suggestions.append(f"Organize joint projects between {dept} and other departments")

        suggestions.append("Consider cross-functional teams for new initiatives")
        suggestions.append("Implement regular interdepartmental meetings or showcases")
        suggestions.append("Create mentorship programs across department boundaries")

        return suggestions[:4]  # Limit to top 4 suggestions


# Convenience function for CLI usage
async def create_insights_agent(settings: Optional[Settings] = None) -> InsightsAgent:
    """Create and initialize an insights agent.

    Args:
        settings: Optional settings instance

    Returns:
        Initialized InsightsAgent
    """
    agent = InsightsAgent(settings)
    await agent.initialize()
    return agent
