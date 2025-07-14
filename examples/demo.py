"""Example script demonstrating the workplace social graph AI agent."""

import asyncio
import logging
from datetime import datetime

from src.agents import InsightsAgent, SocialGraphAgent
from src.config.settings import Settings
from src.database.models import (ContactMethod, Interaction, InteractionType,
                                 Person, RelationshipType, WorkRelationship)


async def setup_sample_data(agent: SocialGraphAgent):
    """Setup sample workplace data."""
    print("🏗️ Setting up sample workplace data...")

    # Add sample people
    people = [
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@company.com",
            "department": "Engineering",
            "role": "Senior Software Engineer",
            "skills": ["Python", "React", "AWS", "Machine Learning"],
            "location": "San Francisco"
        },
        {
            "name": "Bob Smith",
            "email": "bob.smith@company.com",
            "department": "Engineering",
            "role": "DevOps Engineer",
            "skills": ["Docker", "Kubernetes", "AWS", "Terraform"],
            "location": "San Francisco"
        },
        {
            "name": "Carol Williams",
            "email": "carol.williams@company.com",
            "department": "Product",
            "role": "Product Manager",
            "skills": ["Product Strategy", "Data Analysis", "Agile"],
            "location": "New York"
        },
        {
            "name": "David Chen",
            "email": "david.chen@company.com",
            "department": "Design",
            "role": "UX Designer",
            "skills": ["Figma", "User Research", "Prototyping"],
            "location": "Remote"
        },
        {
            "name": "Emily Davis",
            "email": "emily.davis@company.com",
            "department": "Engineering",
            "role": "Engineering Manager",
            "skills": ["Leadership", "Python", "System Design"],
            "location": "San Francisco"
        },
        {
            "name": "Frank Miller",
            "email": "frank.miller@company.com",
            "department": "Sales",
            "role": "Sales Manager",
            "skills": ["Sales Strategy", "CRM", "Negotiation"],
            "location": "Chicago"
        }
    ]

    for person_data in people:
        result = await agent.process_command("add_coworker", **person_data)
        print(f"  Added: {person_data['name']}")

    print("✅ Sample data setup complete!")


async def demonstrate_features(agent: SocialGraphAgent, insights_agent: InsightsAgent):
    """Demonstrate key features of the system."""
    print("\n🚀 Demonstrating Workplace Social Graph AI Agent Features\n")

    # 1. Find experts
    print("1️⃣ Finding Python experts:")
    result = await agent.process_command("find_experts", skill="Python")
    print(result)
    print()

    # 2. Get org chart
    print("2️⃣ Engineering department org chart:")
    result = await agent.process_command("get_org_chart", department="Engineering")
    print(result)
    print()

    # 3. Network insights for a specific person
    print("3️⃣ Network analysis for Alice Johnson:")
    result = await agent.process_command("get_network_insights", person="Alice Johnson")
    print(result)
    print()

    # 4. Who should I ask
    print("4️⃣ Who should I ask about AWS infrastructure?")
    result = await agent.process_command("who_should_i_ask", topic="AWS infrastructure")
    print(result)
    print()

    # 5. Overall network insights
    print("5️⃣ Overall network insights:")
    result = await agent.process_command("get_network_insights")
    print(result)
    print()

    # 6. Daily insights report
    print("6️⃣ Daily insights report:")
    result = await insights_agent.generate_daily_insights()
    print(result)
    print()

    # 7. Identify organizational silos
    print("7️⃣ Organizational silo analysis:")
    result = await insights_agent.identify_silos()
    print(result)
    print()

    # 8. Connection recommendations
    print("8️⃣ Connection recommendations for Alice:")
    result = await insights_agent.recommend_connections("alice.johnson@company.com")
    print(result)
    print()

    # 9. Network statistics
    print("9️⃣ Network statistics:")
    stats = await agent.get_stats()
    print(f"📊 Network Statistics:")
    print(f"• Total people: {stats.get('total_people', 0)}")
    print(f"• Total relationships: {stats.get('total_relationships', 0)}")
    print(f"• Total departments: {stats.get('total_departments', 0)}")
    if 'network_density' in stats:
        print(f"• Network density: {stats['network_density']:.1%}")
    print()


async def demonstrate_chat_interface(agent: SocialGraphAgent):
    """Demonstrate the chat interface."""
    print("💬 Chat Interface Demo:\n")

    chat_examples = [
        "What can you help me with?",
        "Find experts in machine learning",
        "Show me the Engineering org chart",
        "Who should I ask about product strategy?",
        "Analyze network connections for Emily Davis"
    ]

    for question in chat_examples:
        print(f"👤 User: {question}")
        response = await agent.chat(question)
        print(f"🤖 Agent: {response}\n")


async def export_demo(agent: SocialGraphAgent):
    """Demonstrate data export functionality."""
    print("💾 Data Export Demo:")

    # Export to CSV
    result = await agent.process_command(
        "export_data",
        format="csv",
        output_path="./example_export",
        include_sensitive=False
    )
    print(result)


async def main():
    """Main demonstration script."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("🤖 Workplace Social Graph AI Agent Demo")
    print("=====================================\n")

    # Initialize settings (using defaults)
    settings = Settings()

    print(f"🔧 Configuration:")
    print(f"• Neo4j URI: {settings.neo4j_uri}")
    print(f"• Database: {settings.neo4j_database}")
    print(f"• Debug mode: {settings.debug}\n")

    try:
        # Create agents
        async with SocialGraphAgent(settings) as agent:
            async with InsightsAgent(settings) as insights_agent:

                # Setup sample data
                await setup_sample_data(agent)

                # Demonstrate features
                await demonstrate_features(agent, insights_agent)

                # Chat interface demo
                await demonstrate_chat_interface(agent)

                # Export demo
                await export_demo(agent)

                print("🎉 Demo completed successfully!")
                print("\n💡 Next steps:")
                print("• Try the interactive CLI: python -m src.main chat")
                print("• Add your own data: python -m src.main person add --help")
                print("• Explore network insights: python -m src.main network --help")
                print("• Export your data: python -m src.main data export --help")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("• Ensure Neo4j is running: docker-compose up -d")
        print("• Check database connection: python -m src.main setup check-config")
        print("• Initialize database: python -m src.main setup init-db")


if __name__ == "__main__":
    asyncio.run(main())
