"""Agent tools for workplace social graph operations."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..analysis import ExportManager, NetworkAnalyzer
from ..database import (CommunicationPreference, Interaction, InteractionType,
                        Neo4jManager, Person, WorkRelationship,
                        WorkRelationshipType, get_neo4j_manager)

logger = logging.getLogger(__name__)


class WorkplaceTools:
    """Collection of tools for workplace social graph operations."""

    def __init__(self, neo4j_manager: Neo4jManager = None):
        """Initialize workplace tools.

        Args:
            neo4j_manager: Optional Neo4j manager instance
        """
        self.neo4j_manager = neo4j_manager
        self.network_analyzer = None
        self.export_manager = None

    async def _get_neo4j_manager(self) -> Neo4jManager:
        """Get Neo4j manager instance."""
        if not self.neo4j_manager:
            self.neo4j_manager = await get_neo4j_manager()
        return self.neo4j_manager

    async def _get_network_analyzer(self) -> NetworkAnalyzer:
        """Get network analyzer instance."""
        if not self.network_analyzer:
            manager = await self._get_neo4j_manager()
            self.network_analyzer = NetworkAnalyzer(manager)
        return self.network_analyzer

    async def _get_export_manager(self) -> ExportManager:
        """Get export manager instance."""
        if not self.export_manager:
            manager = await self._get_neo4j_manager()
            self.export_manager = ExportManager(manager)
        return self.export_manager

    async def add_coworker(self, name: str, email: str = None, department: str = None, role: str = None, **kwargs) -> str:
        """Add a coworker to the workplace social graph."""
        try:
            # Create Person model
            person = Person(
                name=name,
                role=role,
                department=department,
                email=email,
                phone=kwargs.get("phone"),
                manager=kwargs.get("manager"),
                expertise_areas=kwargs.get("expertise", []),
                communication_preference=CommunicationPreference(kwargs.get("communication_preference")) if kwargs.get("communication_preference") else None,
                timezone=kwargs.get("timezone"),
                notes=kwargs.get("notes")
            )

            # Add to database
            manager_instance = await self._get_neo4j_manager()
            person_id = await manager_instance.add_coworker(person)

            return f"✅ Added {name} successfully to the workplace graph"

        except Exception as e:
            logger.error(f"Failed to add coworker {name}: {e}")
            return f"❌ Failed to add {name}: {str(e)}"

    async def find_experts(self, expertise_area: str, department: str = None, limit: int = 5) -> str:
        """Find subject matter experts by expertise area."""
        try:
            # Get experts from database
            manager_instance = await self._get_neo4j_manager()
            experts = await manager_instance.find_experts(expertise_area, department)

            if not experts:
                return f"🎯 Found 0 expert(s) for '{expertise_area}'"

            # Limit results
            experts = experts[:limit]

            result = f"🎯 Found {len(experts)} expert(s) for '{expertise_area}':\n"
            for expert in experts:
                result += f"• {expert.name} ({expert.department}) - {expert.email}\n"
                if expert.expertise_areas:
                    result += f"  Skills: {', '.join(expert.expertise_areas)}\n"

            return result.strip()

        except Exception as e:
            logger.error(f"Failed to find experts for {expertise_area}: {e}")
            return f"❌ Failed to find experts: {str(e)}"

    async def who_should_i_ask(self, question_topic: str, department: str = None) -> str:
        """Find the right person to ask about a specific topic."""
        try:
            # First, find experts in the topic area
            manager_instance = await self._get_neo4j_manager()
            experts = await manager_instance.find_experts(question_topic, department)

            if experts:
                expert = experts[0]  # Get the top expert
                return f"👥 For '{question_topic}', I recommend asking {expert.name} ({expert.department}) - {expert.email}"

            # If no direct experts, suggest based on department
            if department:
                team_members = await manager_instance.get_team_members(department=department)
                if team_members:
                    member = team_members[0]
                    return f"👥 No specific experts found for '{question_topic}', but you could try asking {member.name} from {department} - {member.email}"

            return f"🤷 No specific experts found for '{question_topic}'. Consider posting in a general team channel."

        except Exception as e:
            logger.error(f"Failed to find who to ask about {question_topic}: {e}")
            return f"❌ Failed to find recommendations: {str(e)}"

    async def get_org_chart(self, department: str = None) -> str:
        """Get organizational chart data."""
        try:
            analyzer = await self._get_network_analyzer()
            org_chart = await analyzer.get_org_chart_data(department)

            if not org_chart:
                return "📊 No organizational structure found"

            return f"📊 Organizational chart generated for {department or 'all departments'}"

        except Exception as e:
            logger.error(f"Failed to get org chart: {e}")
            return f"❌ Failed to generate org chart: {str(e)}"

    async def export_data(self, format: str = "csv", output_path: str = "./export", include_sensitive: bool = False) -> str:
        """Export workplace data."""
        try:
            exporter = await self._get_export_manager()

            if format.lower() == "csv":
                success = await exporter.export_contacts_csv(f"{output_path}/contacts.csv")
                if success:
                    return f"💾 Data exported successfully to {output_path}/contacts.csv"
                else:
                    return "❌ Failed to export data"
            else:
                return f"❌ Unsupported format: {format}"

        except Exception as e:
            logger.error(f"Failed to export data: {e}")
            return f"❌ Failed to export data: {str(e)}"

    async def get_network_insights(self, person: str = None, department: str = None) -> str:
        """Get network insights and analysis."""
        try:
            analyzer = await self._get_network_analyzer()

            # Build the graph
            await analyzer.build_graph_from_neo4j()

            if person:
                metrics = analyzer.calculate_centrality_metrics(person)
                if person in metrics:
                    metric = metrics[person]
                    return f"🔍 Network insights for {person}: Betweenness centrality: {metric.betweenness_centrality:.3f}"

            # General insights
            total_nodes = analyzer.graph.number_of_nodes()
            total_edges = analyzer.graph.number_of_edges()

            return f"🔍 Network insights: {total_nodes} people, {total_edges} connections"

        except Exception as e:
            logger.error(f"Failed to get network insights: {e}")
            return f"❌ Failed to get insights: {str(e)}"


# Tool functions for AI agents

async def add_coworker_tool(
    workplace_tools: WorkplaceTools,
    name: str,
    role: str = None,
    department: str = None,
    email: str = None,
    phone: str = None,
    manager: str = None,
    expertise: List[str] = None,
    communication_preference: str = None,
    timezone: str = None,
    notes: str = None
) -> str:
    """Add a coworker to the workplace social graph.

    Args:
        workplace_tools: WorkplaceTools instance
        name: Full name of the coworker
        role: Job title or role
        department: Department or team
        email: Email address
        phone: Phone number
        manager: Manager's name
        expertise: List of expertise areas
        communication_preference: Preferred communication method
        timezone: Timezone
        notes: Additional notes

    Returns:
        str: Success message with coworker details
    """
    try:
        # Create Person model
        person = Person(
            name=name,
            role=role,
            department=department,
            email=email,
            phone=phone,
            manager=manager,
            expertise_areas=expertise or [],
            communication_preference=CommunicationPreference(communication_preference) if communication_preference else None,
            timezone=timezone,
            notes=notes
        )

        # Add to database
        manager_instance = await workplace_tools._get_neo4j_manager()
        person_id = await manager_instance.add_coworker(person)

        # Create manager relationship if specified
        if manager:
            relationship = WorkRelationship(
                from_person=name,
                to_person=manager,
                relationship_type=WorkRelationshipType.MANAGER,
                bidirectional=False,
                context="Reporting Structure"
            )
            await manager_instance.add_relationship(relationship)

        result = f"✅ Successfully added coworker '{name}'"
        if role:
            result += f" as {role}"
        if department:
            result += f" in {department}"
        if expertise:
            result += f" with expertise in {', '.join(expertise)}"

        return result

    except Exception as e:
        logger.error(f"Error adding coworker: {e}")
        return f"❌ Failed to add coworker '{name}': {str(e)}"


async def add_relationship_tool(
    workplace_tools: WorkplaceTools,
    from_person: str,
    to_person: str,
    relationship_type: str,
    context: str = None,
    strength: float = None,
    bidirectional: bool = True,
    notes: str = None
) -> str:
    """Add a relationship between two coworkers.

    Args:
        workplace_tools: WorkplaceTools instance
        from_person: Name of the first person
        to_person: Name of the second person
        relationship_type: Type of relationship (manager, colleague, client, etc.)
        context: Context of the relationship
        strength: Relationship strength (0.0 to 1.0)
        bidirectional: Whether the relationship is bidirectional
        notes: Additional notes

    Returns:
        str: Success message with relationship details
    """
    try:
        # Validate relationship type
        try:
            rel_type = WorkRelationshipType(relationship_type.lower())
        except ValueError:
            return f"❌ Invalid relationship type '{relationship_type}'. Valid types: {', '.join([t.value for t in WorkRelationshipType])}"

        # Create relationship model
        relationship = WorkRelationship(
            from_person=from_person,
            to_person=to_person,
            relationship_type=rel_type,
            context=context,
            strength=strength,
            bidirectional=bidirectional,
            notes=notes
        )

        # Add to database
        manager = await workplace_tools._get_neo4j_manager()
        success = await manager.add_relationship(relationship)

        if success:
            direction = "bidirectional" if bidirectional else "directional"
            return f"✅ Successfully added {direction} {relationship_type} relationship between '{from_person}' and '{to_person}'"
        else:
            return f"❌ Failed to add relationship between '{from_person}' and '{to_person}'"

    except Exception as e:
        logger.error(f"Error adding relationship: {e}")
        return f"❌ Failed to add relationship: {str(e)}"


async def log_interaction_tool(
    workplace_tools: WorkplaceTools,
    with_person: str,
    interaction_type: str,
    topic: str = None,
    outcome: str = None,
    duration_minutes: int = None,
    project: str = None,
    location: str = None,
    participants: List[str] = None,
    notes: str = None,
    follow_up_required: bool = False,
    follow_up_date: str = None
) -> str:
    """Log an interaction with a coworker.

    Args:
        workplace_tools: WorkplaceTools instance
        with_person: Name of the person interacted with
        interaction_type: Type of interaction (meeting, email, chat, etc.)
        topic: What was discussed
        outcome: Result or next steps
        duration_minutes: Duration in minutes
        project: Related project
        location: Location of interaction
        participants: Other participants
        notes: Additional notes
        follow_up_required: Whether follow-up is needed
        follow_up_date: When to follow up (ISO format)

    Returns:
        str: Success message with interaction details
    """
    try:
        # Validate interaction type
        try:
            int_type = InteractionType(interaction_type.lower())
        except ValueError:
            return f"❌ Invalid interaction type '{interaction_type}'. Valid types: {', '.join([t.value for t in InteractionType])}"

        # Parse follow-up date if provided
        follow_up_datetime = None
        if follow_up_date:
            try:
                follow_up_datetime = datetime.fromisoformat(follow_up_date)
            except ValueError:
                return f"❌ Invalid follow-up date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"

        # Create interaction model
        interaction = Interaction(
            with_person=with_person,
            interaction_type=int_type,
            topic=topic,
            outcome=outcome,
            duration_minutes=duration_minutes,
            project=project,
            location=location,
            participants=participants or [],
            notes=notes,
            follow_up_required=follow_up_required,
            follow_up_date=follow_up_datetime
        )

        # Add to database
        manager = await workplace_tools._get_neo4j_manager()
        success = await manager.add_interaction(interaction)

        if success:
            result = f"✅ Successfully logged {interaction_type} interaction with '{with_person}'"
            if topic:
                result += f" about '{topic}'"
            if duration_minutes:
                result += f" (Duration: {duration_minutes} minutes)"
            if follow_up_required:
                result += f" - Follow-up required"
                if follow_up_date:
                    result += f" by {follow_up_date}"
            return result
        else:
            return f"❌ Failed to log interaction with '{with_person}'"

    except Exception as e:
        logger.error(f"Error logging interaction: {e}")
        return f"❌ Failed to log interaction: {str(e)}"


async def find_experts_tool(
    workplace_tools: WorkplaceTools,
    expertise_area: str,
    department: str = None,
    limit: int = 5
) -> str:
    """Find subject matter experts by expertise area.

    Args:
        workplace_tools: WorkplaceTools instance
        expertise_area: Area of expertise to search for
        department: Optional department filter
        limit: Maximum number of experts to return

    Returns:
        str: List of experts with their details
    """
    try:
        manager = await workplace_tools._get_neo4j_manager()
        experts = await manager.find_experts(expertise_area, department)

        if not experts:
            dept_filter = f" in {department}" if department else ""
            return f"🔍 No experts found for '{expertise_area}'{dept_filter}"

        # Limit results
        experts = experts[:limit]

        result = f"🎯 Found {len(experts)} expert(s) for '{expertise_area}':\n\n"

        for expert in experts:
            result += f"👤 **{expert.name}**"
            if expert.role:
                result += f" - {expert.role}"
            if expert.department:
                result += f" ({expert.department})"
            result += "\n"

            if expert.email:
                result += f"   📧 {expert.email}\n"

            if expert.expertise_areas:
                other_skills = [skill for skill in expert.expertise_areas if expertise_area.lower() not in skill.lower()]
                if other_skills:
                    result += f"   🛠️ Other expertise: {', '.join(other_skills[:3])}\n"

            if expert.communication_preference:
                result += f"   💬 Prefers: {expert.communication_preference}\n"

            result += "\n"

        return result.strip()

    except Exception as e:
        logger.error(f"Error finding experts: {e}")
        return f"❌ Failed to find experts for '{expertise_area}': {str(e)}"


async def who_should_i_ask_tool(
    workplace_tools: WorkplaceTools,
    question_topic: str,
    department: str = None
) -> str:
    """Find the right person to ask about a specific topic.

    Args:
        workplace_tools: WorkplaceTools instance
        question_topic: The topic or question you need help with
        department: Optional department to focus on

    Returns:
        str: Recommendations for who to contact
    """
    try:
        # First, find experts in the topic area
        manager = await workplace_tools._get_neo4j_manager()
        experts = await manager.find_experts(question_topic, department)

        if not experts:
            # Try broader search by splitting the topic
            topic_words = question_topic.split()
            for word in topic_words:
                if len(word) > 3:  # Skip short words
                    experts = await manager.find_experts(word, department)
                    if experts:
                        break

        if not experts:
            dept_filter = f" in {department}" if department else ""
            return f"🤔 I couldn't find specific experts for '{question_topic}'{dept_filter}. You might want to ask in your team or search by related keywords."

        # Get network analysis for additional context
        network_analyzer = await workplace_tools._get_network_analyzer()
        await network_analyzer.build_graph_from_neo4j()

        result = f"💡 For questions about '{question_topic}', I recommend contacting:\n\n"

        # Prioritize experts by connectivity and role
        for i, expert in enumerate(experts[:3]):  # Top 3 recommendations
            result += f"{i+1}. **{expert.name}**"
            if expert.role:
                result += f" - {expert.role}"
            if expert.department:
                result += f" ({expert.department})"
            result += "\n"

            if expert.email:
                result += f"   📧 {expert.email}\n"

            # Add connection suggestions
            if network_analyzer.graph and expert.name in network_analyzer.graph:
                connections = list(network_analyzer.graph.neighbors(expert.name))
                if connections:
                    result += f"   🔗 Well-connected with {len(connections)} colleagues\n"

            if expert.communication_preference:
                result += f"   💬 Best contact method: {expert.communication_preference}\n"

            # Suggest why they're a good choice
            matching_skills = [skill for skill in expert.expertise_areas if question_topic.lower() in skill.lower()]
            if matching_skills:
                result += f"   ✅ Expert in: {', '.join(matching_skills)}\n"

            result += "\n"

        # Add knowledge broker suggestions
        if network_analyzer.graph:
            brokers = network_analyzer.find_knowledge_brokers(question_topic)
            if brokers:
                result += f"🌉 **Alternative contacts** (knowledge brokers who can connect you):\n"
                for broker in brokers[:2]:  # Top 2 brokers
                    broker_data = network_analyzer.graph.nodes.get(broker, {})
                    result += f"• {broker}"
                    if broker_data.get('role'):
                        result += f" ({broker_data['role']})"
                    result += " - Can introduce you to the right experts\n"

        return result.strip()

    except Exception as e:
        logger.error(f"Error in who_should_i_ask: {e}")
        return f"❌ Failed to find recommendations for '{question_topic}': {str(e)}"


async def get_org_chart_tool(
    workplace_tools: WorkplaceTools,
    department: str = None,
    person: str = None
) -> str:
    """Get organizational chart information.

    Args:
        workplace_tools: WorkplaceTools instance
        department: Optional department filter
        person: Optional specific person to show hierarchy for

    Returns:
        str: Organizational chart information
    """
    try:
        manager = await workplace_tools._get_neo4j_manager()

        if person:
            # Show specific person's position in hierarchy
            reporting_chain = await manager.get_reporting_chain(person)
            direct_reports = await manager.get_direct_reports(person)

            result = f"📊 Organizational position for **{person}**:\n\n"

            if reporting_chain:
                result += "⬆️ **Reports to:**\n"
                for i, manager_person in enumerate(reporting_chain):
                    indent = "  " * (i + 1)
                    result += f"{indent}• {manager_person.name}"
                    if manager_person.role:
                        result += f" ({manager_person.role})"
                    result += "\n"
                result += "\n"

            if direct_reports:
                result += "⬇️ **Direct Reports:**\n"
                for report in direct_reports:
                    result += f"  • {report.name}"
                    if report.role:
                        result += f" ({report.role})"
                    result += "\n"
            else:
                result += "⬇️ **Direct Reports:** None (Individual Contributor)\n"

            return result.strip()

        else:
            # Show department or full org chart
            team_members = await manager.get_team_members(department=department)

            if not team_members:
                filter_desc = f" in {department}" if department else ""
                return f"📊 No team members found{filter_desc}"

            # Group by role/hierarchy
            managers = {}
            individual_contributors = []

            for member in team_members:
                if member.manager:
                    if member.manager not in managers:
                        managers[member.manager] = []
                    managers[member.manager].append(member)
                else:
                    individual_contributors.append(member)

            title = f"📊 Organizational Chart"
            if department:
                title += f" - {department} Department"
            result = f"{title}:\n\n"

            # Show management hierarchy
            if managers:
                result += "👥 **Teams by Manager:**\n\n"
                for manager_name, reports in managers.items():
                    result += f"**{manager_name}** (Manager)\n"
                    for report in reports:
                        result += f"  └── {report.name}"
                        if report.role:
                            result += f" - {report.role}"
                        result += "\n"
                    result += "\n"

            # Show individual contributors
            if individual_contributors:
                result += "👤 **Individual Contributors:**\n"
                for ic in individual_contributors:
                    result += f"• {ic.name}"
                    if ic.role:
                        result += f" - {ic.role}"
                    result += "\n"

            result += f"\n📈 **Total Team Size:** {len(team_members)} people"

            return result.strip()

    except Exception as e:
        logger.error(f"Error getting org chart: {e}")
        return f"❌ Failed to get organizational chart: {str(e)}"


async def get_network_insights_tool(
    workplace_tools: WorkplaceTools,
    person: str = None,
    department: str = None
) -> str:
    """Get network analysis insights for a person or department.

    Args:
        workplace_tools: WorkplaceTools instance
        person: Optional specific person to analyze
        department: Optional department to analyze

    Returns:
        str: Network analysis insights
    """
    try:
        network_analyzer = await workplace_tools._get_network_analyzer()
        await network_analyzer.build_graph_from_neo4j()

        if person:
            # Individual analysis
            if person not in network_analyzer.graph:
                return f"👤 Person '{person}' not found in the network"

            metrics = network_analyzer.calculate_centrality_metrics(person)
            person_metrics = metrics[person]

            result = f"🔍 **Network Analysis for {person}:**\n\n"

            result += f"🔗 **Connections:** {person_metrics.total_connections} direct connections\n"
            result += f"📈 **Influence Score:** {person_metrics.degree_centrality:.3f} (0-1 scale)\n"
            result += f"🌉 **Bridge Score:** {person_metrics.betweenness_centrality:.3f} (how much you connect others)\n"
            result += f"🎯 **Reach Score:** {person_metrics.closeness_centrality:.3f} (how easily you can reach others)\n\n"

            # Categorize influence level
            if person_metrics.degree_centrality > 0.3:
                result += "🌟 **Status:** Highly influential in the network\n"
            elif person_metrics.degree_centrality > 0.15:
                result += "⭐ **Status:** Moderately influential in the network\n"
            else:
                result += "💼 **Status:** Focused role with targeted connections\n"

            # Bridge analysis
            if person_metrics.betweenness_centrality > 0.1:
                result += "🌉 **Role:** Key connector - you bridge different groups\n"

            return result.strip()

        else:
            # Department or overall analysis
            if department:
                dept_metrics = network_analyzer.analyze_department_connectivity()
                if department not in dept_metrics:
                    return f"🏢 Department '{department}' not found in the network"

                dept_data = dept_metrics[department]
                result = f"🏢 **Network Analysis for {department} Department:**\n\n"

                result += f"👥 **Team Size:** {dept_data['member_count']} people\n"
                result += f"🔗 **Internal Connections:** {dept_data['internal_connections']}\n"
                result += f"🌐 **External Connections:** {dept_data['external_connections']}\n"
                result += f"📊 **Team Cohesion:** {dept_data['internal_density']:.2%}\n"
                result += f"🤝 **External Collaboration:** {dept_data['avg_external_connections_per_person']:.1f} connections per person\n\n"

                # Assessment
                if dept_data['internal_density'] > 0.5:
                    result += "✅ **Assessment:** Highly cohesive team with strong internal collaboration\n"
                elif dept_data['internal_density'] > 0.3:
                    result += "⚖️ **Assessment:** Moderately connected team\n"
                else:
                    result += "📈 **Assessment:** Opportunity to improve internal team connections\n"

            else:
                # Overall network insights
                influential_people = network_analyzer.find_influential_people(top_n=5)
                dept_connectivity = network_analyzer.analyze_department_connectivity()

                result = "🌐 **Overall Network Insights:**\n\n"

                result += "🌟 **Most Influential People:**\n"
                for i, (person, score) in enumerate(influential_people):
                    result += f"{i+1}. {person} (influence: {score:.3f})\n"
                result += "\n"

                result += "🏢 **Department Connectivity:**\n"
                for dept, data in sorted(dept_connectivity.items(), key=lambda x: x[1]['member_count'], reverse=True)[:5]:
                    result += f"• {dept}: {data['member_count']} people, {data['internal_density']:.1%} cohesion\n"

                result += f"\n📊 **Network Size:** {len(network_analyzer.graph.nodes())} people total"

            return result.strip()

    except Exception as e:
        logger.error(f"Error getting network insights: {e}")
        return f"❌ Failed to get network insights: {str(e)}"


async def export_data_tool(
    workplace_tools: WorkplaceTools,
    format: str = "csv",
    output_path: str = "./export",
    include_sensitive: bool = False
) -> str:
    """Export workplace social graph data.

    Args:
        workplace_tools: Instance of WorkplaceTools
        format: Export format (csv, json, excel)
        output_path: Output directory path
        include_sensitive: Whether to include sensitive data

    Returns:
        str: Success message with file paths
    """
    try:
        export_manager = await workplace_tools._get_export_manager()

        # Create output directory if it doesn't exist
        from pathlib import Path
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        exported_files = []

        if format.lower() == "csv":
            # Export contacts
            contacts_file = output_dir / f"contacts_{timestamp}.csv"
            await export_manager.export_contacts_csv(contacts_file, include_personal_notes=include_sensitive)
            exported_files.append(str(contacts_file))

            # Export interactions if sensitive data is requested
            if include_sensitive:
                interactions_file = output_dir / f"interactions_{timestamp}.csv"
                await export_manager.export_interactions_csv(interactions_file)
                exported_files.append(str(interactions_file))

        elif format.lower() == "json":
            # Export network structure
            network_file = output_dir / f"network_{timestamp}.json"
            await export_manager.export_network_json(network_file, include_sensitive_data=include_sensitive)
            exported_files.append(str(network_file))

        elif format.lower() == "excel":
            # Export comprehensive Excel file
            excel_file = output_dir / f"workplace_data_{timestamp}.xlsx"
            await export_manager.export_comprehensive_excel(excel_file, include_sensitive_data=include_sensitive)
            exported_files.append(str(excel_file))

        else:
            return f"❌ Unsupported format: {format}. Supported formats: csv, json, excel"

        result = f"✅ **Data Export Successful**\n\n"
        result += f"📁 **Export Directory:** {output_path}\n"
        result += f"📄 **Format:** {format.upper()}\n"
        result += f"🔒 **Sensitive Data:** {'Included' if include_sensitive else 'Excluded'}\n\n"
        result += "📋 **Exported Files:**\n"

        for file_path in exported_files:
            result += f"• {Path(file_path).name}\n"

        return result.strip()

    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        return f"❌ Failed to export data: {str(e)}"
