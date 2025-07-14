"""Main AI agent for workplace social graph management."""

import asyncio
import logging
from typing import Any, Dict, Optional

from ..analysis.export_manager import ExportManager
from ..analysis.network_analysis import NetworkAnalyzer
from ..config.settings import Settings
from ..database.neo4j_manager import Neo4jManager
from .tools import (WorkplaceTools, add_coworker_tool, export_data_tool,
                    find_experts_tool, get_network_insights_tool,
                    get_org_chart_tool, who_should_i_ask_tool)

logger = logging.getLogger(__name__)


class SocialGraphAgent:
    """Main AI agent for workplace social graph management."""

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the social graph agent.

        Args:
            settings: Optional settings instance
        """
        self.settings = settings or Settings()
        self.neo4j_manager = Neo4jManager(self.settings)
        self.workplace_tools = WorkplaceTools(
            neo4j_manager=self.neo4j_manager
        )

    async def __aenter__(self):
        """Async context manager entry."""
        try:
            await self.neo4j_manager.connect()
            logger.info("Neo4j connection established successfully")
        except Exception as e:
            logger.warning(f"Failed to connect to Neo4j: {e}")
            logger.info("Agent will run in offline mode")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.neo4j_manager.close()

    async def initialize(self):
        """Initialize the agent and ensure database connectivity."""
        await self.neo4j_manager.connect()
        logger.info("Social graph agent initialized successfully")

    async def close(self):
        """Close database connections."""
        await self.neo4j_manager.close()
        logger.info("Social graph agent closed")

    async def process_command(self, command: str, **kwargs) -> str:
        """Process a command through the appropriate tool.

        Args:
            command: The command to process
            **kwargs: Additional arguments for the command

        Returns:
            str: Result of the command execution
        """
        try:
            command = command.lower().strip()

            if command == "add_coworker":
                return await self.workplace_tools.add_coworker(
                    name=kwargs.get("name"),
                    email=kwargs.get("email"),
                    department=kwargs.get("department"),
                    role=kwargs.get("role"),
                    expertise=kwargs.get("skills", []),
                    phone=kwargs.get("phone"),
                    manager=kwargs.get("manager")
                )

            elif command == "find_experts":
                return await self.workplace_tools.find_experts(
                    expertise_area=kwargs.get("skill") or kwargs.get("expertise_area"),
                    department=kwargs.get("department"),
                    limit=kwargs.get("limit", 5)
                )

            elif command == "who_should_i_ask":
                return await self.workplace_tools.who_should_i_ask(
                    question_topic=kwargs.get("topic") or kwargs.get("question_topic"),
                    department=kwargs.get("department")
                )

            elif command == "get_org_chart":
                return await self.workplace_tools.get_org_chart(
                    department=kwargs.get("department")
                )

            elif command == "export_data":
                return await self.workplace_tools.export_data(
                    format=kwargs.get("format", "csv"),
                    output_path=kwargs.get("output_path", "./export"),
                    include_sensitive=kwargs.get("include_sensitive", False)
                )

            elif command == "get_network_insights":
                return await self.workplace_tools.get_network_insights(
                    person=kwargs.get("person"),
                    department=kwargs.get("department")
                )

            else:
                return f"❌ Unknown command: {command}. Available commands: add_coworker, find_experts, who_should_i_ask, get_org_chart, export_data, get_network_insights"

        except Exception as e:
            logger.error(f"Error processing command '{command}': {e}")
            return f"❌ Error processing command: {str(e)}"

    async def chat(self, message: str) -> str:
        """Process a natural language message and determine the appropriate action.

        Args:
            message: Natural language message from user

        Returns:
            str: Response from the agent
        """
        try:
            message_lower = message.lower()

            # Simple intent recognition (could be enhanced with more sophisticated NLP)
            if any(phrase in message_lower for phrase in ["add", "new coworker", "introduce"]):
                return ("👋 To add a new coworker, I need some information. Please use the command:\n"
                       "add_coworker with name, email, department, and role at minimum.\n"
                       "Example: add_coworker name='John Doe' email='john@company.com' department='Engineering' role='Senior Developer'")

            elif any(phrase in message_lower for phrase in ["expert", "who knows", "find someone"]):
                return ("🔍 I can help you find experts! Please specify the skill or expertise area you're looking for.\n"
                       "Example: find_experts skill='Python' or who_should_i_ask topic='machine learning'")

            elif any(phrase in message_lower for phrase in ["org chart", "organization", "hierarchy"]):
                return ("🏢 I can show you the organizational structure. Use:\n"
                       "get_org_chart to see the overall structure, or\n"
                       "get_org_chart department='Engineering' for a specific department")

            elif any(phrase in message_lower for phrase in ["network", "connections", "influence"]):
                return ("📊 I can analyze network connections and influence. Use:\n"
                       "get_network_insights for overall network analysis, or\n"
                       "get_network_insights person='John Doe' for individual analysis, or\n"
                       "get_network_insights department='Engineering' for department analysis")

            elif any(phrase in message_lower for phrase in ["export", "download", "backup"]):
                return ("💾 I can export data in various formats. Use:\n"
                       "export_data format='csv' output_path='./my_export' to export data\n"
                       "Available formats: csv, json")

            elif any(phrase in message_lower for phrase in ["help", "what can you do", "commands"]):
                return self._get_help_message()

            else:
                return ("🤔 I'm not sure what you'd like me to do. Here are the main things I can help with:\n\n"
                       "• **Add coworkers** - Introduce new team members to the network\n"
                       "• **Find experts** - Locate people with specific skills or knowledge\n"
                       "• **Get recommendations** - Find who to ask about topics\n"
                       "• **Show org chart** - Display organizational structure\n"
                       "• **Analyze networks** - Understand connections and influence\n"
                       "• **Export data** - Download information in various formats\n\n"
                       "Type 'help' for more detailed commands!")

        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            return f"❌ Sorry, I encountered an error: {str(e)}"

    def _get_help_message(self) -> str:
        """Get comprehensive help message."""
        return """🤖 **Workplace Social Graph AI Agent Help**

I help you manage and explore your workplace social network! Here's what I can do:

**👥 People Management:**
• `add_coworker` - Add new team members with skills and relationships
• `find_experts` - Find people with specific skills or expertise
• `who_should_i_ask` - Get recommendations for who to contact about topics

**🏢 Organization:**
• `get_org_chart` - View organizational hierarchy and structure
• `get_network_insights` - Analyze network connections and influence

**📊 Data & Export:**
• `export_data` - Export network data in CSV or JSON format
• Network analysis with centrality metrics and department connectivity

**💡 Tips:**
• Be specific with skills when finding experts (e.g., "Python", "project management")
• Include department names for targeted searches
• All data respects privacy settings and access controls

**Examples:**
• "Find experts in machine learning"
• "Who should I ask about budget planning?"
• "Show me the Engineering org chart"
• "Analyze network connections for Sarah Johnson"

Just tell me what you'd like to do in natural language, and I'll help guide you!"""

    async def get_stats(self) -> Dict[str, Any]:
        """Get current network statistics.

        Returns:
            Dict with network statistics
        """
        try:
            # Get basic counts
            people_count = await self.neo4j_manager.count_people()
            relationships_count = await self.neo4j_manager.count_relationships()

            # Get network analyzer for more detailed stats
            network_analyzer = await self.workplace_tools._get_network_analyzer()
            await network_analyzer.build_graph_from_neo4j()

            # Department distribution
            dept_stats = network_analyzer.analyze_department_connectivity()

            return {
                "total_people": people_count,
                "total_relationships": relationships_count,
                "total_departments": len(dept_stats),
                "network_density": network_analyzer.calculate_network_density(),
                "largest_department": max(dept_stats.items(), key=lambda x: x[1]["member_count"])[0] if dept_stats else None,
                "departments": {dept: data["member_count"] for dept, data in dept_stats.items()}
            }

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"error": str(e)}


# Convenience function for CLI usage
async def create_agent(settings: Optional[Settings] = None) -> SocialGraphAgent:
    """Create and initialize a social graph agent.

    Args:
        settings: Optional settings instance

    Returns:
        Initialized SocialGraphAgent
    """
    agent = SocialGraphAgent(settings)
    await agent.initialize()
    return agent


# For interactive usage
if __name__ == "__main__":
    async def main():
        """Example usage of the social graph agent."""
        async with SocialGraphAgent() as agent:
            print("🤖 Social Graph Agent initialized!")

            # Get current stats
            stats = await agent.get_stats()
            print(f"📊 Network Stats: {stats}")

            # Example chat interaction
            response = await agent.chat("What can you help me with?")
            print(f"\n🤖: {response}")

    asyncio.run(main())
