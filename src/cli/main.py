"""Command-line interface for the workplace social graph AI agent."""

import asyncio
import json
from pathlib import Path
from typing import Optional

import click

from ..agents import InsightsAgent, SocialGraphAgent
from ..config.settings import Settings
from ..database.migrations import initialize_database


@click.group()
@click.option('--config', type=click.Path(), help='Path to configuration file')
@click.pass_context
def cli(ctx, config):
    """Workplace Social Graph AI Agent CLI.

    Manage and explore your workplace social network using AI-powered insights.
    """
    # Initialize context
    ctx.ensure_object(dict)

    # Load settings
    if config:
        # Load from file if provided
        settings = Settings(_env_file=config)
    else:
        settings = Settings()

    ctx.obj['settings'] = settings


@cli.group()
@click.pass_context
def person(ctx):
    """Manage people in the workplace social graph."""
    pass


@person.command('add')
@click.option('--name', required=True, help='Full name of the person')
@click.option('--email', required=True, help='Email address')
@click.option('--department', required=True, help='Department name')
@click.option('--role', required=True, help='Job role/title')
@click.option('--skills', multiple=True, help='Skills (can be used multiple times)')
@click.option('--location', help='Office location')
@click.option('--manager', help='Manager email address')
@click.pass_context
def add_person(ctx, name, email, department, role, skills, location, manager):
    """Add a new person to the social graph."""
    async def _add_person():
        async with SocialGraphAgent(ctx.obj['settings']) as agent:
            result = await agent.process_command(
                'add_coworker',
                name=name,
                email=email,
                department=department,
                role=role,
                skills=list(skills),
                location=location,
                manager=manager
            )
            click.echo(result)

    asyncio.run(_add_person())


@person.command('find-experts')
@click.option('--skill', required=True, help='Skill to search for')
@click.option('--department', help='Limit search to specific department')
@click.option('--limit', default=5, help='Maximum number of results')
@click.pass_context
def find_experts(ctx, skill, department, limit):
    """Find experts with specific skills."""
    async def _find_experts():
        async with SocialGraphAgent(ctx.obj['settings']) as agent:
            result = await agent.process_command(
                'find_experts',
                skill=skill,
                department=department,
                limit=limit
            )
            click.echo(result)

    asyncio.run(_find_experts())


@person.command('who-to-ask')
@click.option('--topic', required=True, help='Topic or question to ask about')
@click.option('--expertise', help='Specific expertise area')
@click.pass_context
def who_to_ask(ctx, topic, expertise):
    """Get recommendations for who to ask about a topic."""
    async def _who_to_ask():
        async with SocialGraphAgent(ctx.obj['settings']) as agent:
            result = await agent.process_command(
                'who_should_i_ask',
                topic=topic,
                expertise_area=expertise
            )
            click.echo(result)

    asyncio.run(_who_to_ask())


@cli.group()
@click.pass_context
def org(ctx):
    """Organizational structure and analysis."""
    pass


@org.command('chart')
@click.option('--department', help='Show chart for specific department')
@click.pass_context
def org_chart(ctx, department):
    """Display organizational chart."""
    async def _org_chart():
        async with SocialGraphAgent(ctx.obj['settings']) as agent:
            result = await agent.process_command(
                'get_org_chart',
                department=department
            )
            click.echo(result)

    asyncio.run(_org_chart())


@cli.group()
@click.pass_context
def network(ctx):
    """Network analysis and insights."""
    pass


@network.command('insights')
@click.option('--person', help='Analyze specific person')
@click.option('--department', help='Analyze specific department')
@click.pass_context
def network_insights(ctx, person, department):
    """Get network analysis insights."""
    async def _network_insights():
        async with SocialGraphAgent(ctx.obj['settings']) as agent:
            result = await agent.process_command(
                'get_network_insights',
                person=person,
                department=department
            )
            click.echo(result)

    asyncio.run(_network_insights())


@network.command('daily-report')
@click.pass_context
def daily_report(ctx):
    """Generate daily network insights report."""
    async def _daily_report():
        async with InsightsAgent(ctx.obj['settings']) as agent:
            result = await agent.generate_daily_insights()
            click.echo(result)

    asyncio.run(_daily_report())


@network.command('collaboration')
@click.option('--days', default=30, help='Number of days to analyze')
@click.pass_context
def collaboration_analysis(ctx, days):
    """Analyze collaboration patterns."""
    async def _collaboration():
        async with InsightsAgent(ctx.obj['settings']) as agent:
            result = await agent.analyze_collaboration_patterns(days_back=days)
            click.echo(result)

    asyncio.run(_collaboration())


@network.command('silos')
@click.pass_context
def identify_silos(ctx):
    """Identify organizational silos."""
    async def _silos():
        async with InsightsAgent(ctx.obj['settings']) as agent:
            result = await agent.identify_silos()
            click.echo(result)

    asyncio.run(_silos())


@network.command('recommend-connections')
@click.option('--email', required=True, help='Email of person to make recommendations for')
@click.option('--limit', default=5, help='Number of recommendations')
@click.pass_context
def recommend_connections(ctx, email, limit):
    """Recommend new connections for a person."""
    async def _recommend():
        async with InsightsAgent(ctx.obj['settings']) as agent:
            result = await agent.recommend_connections(email, limit)
            click.echo(result)

    asyncio.run(_recommend())


@cli.group()
@click.pass_context
def data(ctx):
    """Data management and export."""
    pass


@data.command('export')
@click.option('--format', type=click.Choice(['csv', 'json']), default='csv', help='Export format')
@click.option('--output', default='./export', help='Output directory')
@click.option('--include-sensitive', is_flag=True, help='Include sensitive data')
@click.pass_context
def export_data(ctx, format, output, include_sensitive):
    """Export network data."""
    async def _export():
        async with SocialGraphAgent(ctx.obj['settings']) as agent:
            result = await agent.process_command(
                'export_data',
                format=format,
                output_path=output,
                include_sensitive=include_sensitive
            )
            click.echo(result)

    asyncio.run(_export())


@data.command('stats')
@click.pass_context
def show_stats(ctx):
    """Show network statistics."""
    async def _stats():
        async with SocialGraphAgent(ctx.obj['settings']) as agent:
            stats = await agent.get_stats()

            click.echo("📊 **Network Statistics:**")
            click.echo(f"• Total people: {stats.get('total_people', 0)}")
            click.echo(f"• Total relationships: {stats.get('total_relationships', 0)}")
            click.echo(f"• Total departments: {stats.get('total_departments', 0)}")

            if 'network_density' in stats:
                click.echo(f"• Network density: {stats['network_density']:.1%}")

            if 'largest_department' in stats and stats['largest_department']:
                click.echo(f"• Largest department: {stats['largest_department']}")

            if 'departments' in stats and stats['departments']:
                click.echo("\n🏢 **Department Breakdown:**")
                for dept, count in sorted(stats['departments'].items(), key=lambda x: x[1], reverse=True):
                    click.echo(f"• {dept}: {count} people")

    asyncio.run(_stats())


@cli.group()
@click.pass_context
def setup(ctx):
    """Setup and initialization commands."""
    pass


@setup.command('init-db')
@click.pass_context
def init_database(ctx):
    """Initialize the database schema."""
    async def _init_db():
        settings = ctx.obj['settings']
        try:
            await initialize_database()
            click.echo("✅ Database initialized successfully!")
        except Exception as e:
            click.echo(f"❌ Database initialization failed: {e}")
            raise click.ClickException(str(e))

    asyncio.run(_init_db())


@setup.command('check-config')
@click.pass_context
def check_config(ctx):
    """Check configuration settings."""
    settings = ctx.obj['settings']

    click.echo("🔧 **Configuration Check:**")
    click.echo(f"• Neo4j URI: {settings.neo4j_uri}")
    click.echo(f"• Neo4j Database: {settings.neo4j_database}")
    click.echo(f"• Debug Mode: {settings.debug}")
    click.echo(f"• Log Level: {settings.log_level}")

    # Test database connection
    async def _test_connection():
        try:
            from ..database.neo4j_manager import Neo4jManager
            manager = Neo4jManager(settings)
            await manager.connect()
            await manager.close()
            click.echo("✅ Neo4j connection: OK")
        except Exception as e:
            click.echo(f"❌ Neo4j connection: FAILED - {e}")

    asyncio.run(_test_connection())


@cli.command('chat')
@click.pass_context
def interactive_chat(ctx):
    """Start interactive chat with the AI agent."""
    click.echo("🔄 Starting chat command...")

    async def _chat():
        try:
            click.echo("🔄 Initializing AI agent...")
            click.echo(f"🔄 Settings: {ctx.obj['settings']}")

            async with SocialGraphAgent(ctx.obj['settings']) as agent:
                click.echo("🤖 Welcome to the Workplace Social Graph AI Agent!")
                click.echo("Type 'help' for available commands, or 'quit' to exit.")
                click.echo("")

                while True:
                    try:
                        user_input = click.prompt("You", type=str)

                        if user_input.lower() in ['quit', 'exit', 'bye']:
                            click.echo("👋 Goodbye!")
                            break

                        response = await agent.chat(user_input)
                        click.echo(f"\n🤖 {response}\n")

                    except (KeyboardInterrupt, EOFError):
                        click.echo("\n👋 Goodbye!")
                        break
                    except Exception as e:
                        click.echo(f"❌ Error: {e}")
                        import traceback
                        click.echo(f"Traceback: {traceback.format_exc()}")
        except Exception as e:
            click.echo(f"❌ Failed to initialize agent: {e}")
            import traceback
            click.echo(f"Traceback: {traceback.format_exc()}")

    click.echo("🔄 About to run asyncio...")
    asyncio.run(_chat())
    click.echo("🔄 Asyncio completed.")


if __name__ == '__main__':
    cli()
