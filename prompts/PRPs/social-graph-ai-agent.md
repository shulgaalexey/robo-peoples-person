name: "Social Graph AI Agent System"
description: |

## Purpose
Build a comprehensive AI agent system that maintains and processes social graphs, allowing users to add people, manage relationships, and gain insights through an interactive CLI. The system utilizes Neo4j for graph database backend, LangGraph for graph processing, and provides network analysis capabilities with exportable reports.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **GitHub Copilot Integration**: Leverage GitHub Copilot and its agent mode for code generation
6. **Windows/PowerShell Compatibility**: All commands and scripts should work on Windows with PowerShell

---

## Goal
Build a local-only AI agent system that helps manage work-related relationships and social interactions. The system enables you to track coworkers, their roles, relationships between team members, and intelligently query for insights about professional networks to improve collaboration and communication.

## Why
- **Business value**: Improves workplace relationship management and team collaboration effectiveness
- **Personal productivity**: Helps remember important details about coworkers, their expertise, and interpersonal dynamics
- **Integration**: Demonstrates modern Python development with AI agents, graph databases, and CLI interfaces
- **Problems solved**: Eliminates manual tracking of work relationships, provides intelligent insights about team dynamics, and helps identify key people for specific projects or expertise areas

## What
A comprehensive workplace relationship management system featuring:
- **Personal work network tracking**: Add coworkers with roles, departments, expertise areas, and contact preferences
- **Relationship mapping**: Track professional relationships (manager, direct report, collaborator, mentor, etc.) and interaction history
- **Intelligent querying**: Natural language queries like "Who should I talk to about machine learning projects?" or "What's the best way to reach Sarah about the Q2 planning?"
- **Work context insights**: Identify subject matter experts, communication patterns, and collaboration opportunities
- **Privacy-focused**: Local-only storage with no data leaving your machine
- **Interactive CLI**: Both command-based and chat-based interactions for different use cases

### Success Criteria
- [ ] CLI accepts commands to add coworkers with work-specific attributes (role, department, expertise, etc.)
- [ ] Track various professional relationship types and interaction history
- [ ] Natural language queries return relevant coworkers and relationship insights
- [ ] Export functionality for sharing organizational charts or collaboration maps
- [ ] AI agent provides intelligent suggestions for who to contact for specific work needs
- [ ] All tests pass with >80% coverage
- [ ] System works entirely offline (local-only, privacy-preserving)

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://neo4j.com/docs/api/python-driver/current/
  why: Neo4j Python driver patterns, connection management, Cypher queries

- url: https://neo4j.com/docs/python-manual/current/
  why: Best practices for Neo4j application development

- url: https://langchain-ai.github.io/langgraph/concepts/why-langgraph/
  why: LangGraph fundamentals for graph processing workflows

- url: https://click.palletsprojects.com/
  why: CLI framework patterns, command groups, parameter handling

- url: https://realpython.com/python-click/
  why: Advanced Click patterns for complex CLI applications

- url: https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python
  why: NetworkX patterns for social network analysis and centrality metrics

- url: https://memgraph.com/blog/community-detection-algorithms-with-python-networkx
  why: Community detection algorithms with NetworkX implementation examples

- file: prompts/PLANNING.md
  why: Project architecture, coding standards, file organization patterns

- file: prompts/PRPs/EXAMPLE_multi_agent_prp.md
  why: Multi-agent system patterns, tool integration, async operations

- file: .env.example
  why: Configuration patterns, environment variable management

- file: pyproject.toml
  why: Dependency management, project structure, development tools setup
```

### Current Codebase tree
```powershell
robo-peoples-person/
├── .github/
│   └── copilot-instructions.md
├── prompts/
│   ├── commands/
│   ├── examples/
│   ├── PRPs/
│   ├── INITIAL.md
│   ├── PLANNING.md
│   └── TASK.md
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

### Desired Codebase tree with files to be added and responsibility of file
```powershell
robo-peoples-person/
├── src/
│   ├── __init__.py                    # Package initialization
│   ├── main.py                       # CLI entry point and command router
│   ├── agents/
│   │   ├── __init__.py               # Agent package initialization
│   │   ├── social_graph_agent.py     # Main AI agent for social graph operations
│   │   ├── insights_agent.py         # Specialized agent for network analysis
│   │   └── tools.py                  # Agent tools for graph operations
│   ├── database/
│   │   ├── __init__.py               # Database package initialization
│   │   ├── neo4j_manager.py          # Neo4j connection and query management
│   │   ├── models.py                 # Pydantic models for Person and Relationship
│   │   └── migrations.py             # Database schema setup and migrations
│   ├── analysis/
│   │   ├── __init__.py               # Analysis package initialization
│   │   ├── network_analysis.py       # NetworkX integration for graph metrics
│   │   └── export_manager.py         # JSON/CSV export functionality
│   ├── cli/
│   │   ├── __init__.py               # CLI package initialization
│   │   ├── commands.py               # Click command definitions
│   │   ├── chat.py                   # Interactive chat interface
│   │   └── utils.py                  # CLI utilities and formatters
│   └── config/
│       ├── __init__.py               # Config package initialization
│       └── settings.py               # Pydantic Settings for configuration
├── tests/
│   ├── __init__.py                   # Test package initialization
│   ├── test_agents/
│   │   ├── __init__.py
│   │   ├── test_social_graph_agent.py
│   │   └── test_insights_agent.py
│   ├── test_database/
│   │   ├── __init__.py
│   │   ├── test_neo4j_manager.py
│   │   └── test_models.py
│   ├── test_analysis/
│   │   ├── __init__.py
│   │   ├── test_network_analysis.py
│   │   └── test_export_manager.py
│   ├── test_cli/
│   │   ├── __init__.py
│   │   ├── test_commands.py
│   │   └── test_chat.py
│   └── conftest.py                   # Pytest configuration and fixtures
├── docker-compose.yml                # Neo4j local development setup
└── .env.local                       # Local environment configuration (gitignored)
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: Neo4j driver requires async context management
# Example: Always use async with driver.session() as session:

# CRITICAL: LangGraph requires specific node/edge definitions
# Example: Must define StateGraph with proper TypedDict state

# CRITICAL: Click commands need proper async handling
# Example: Use asyncio.run() for async command functions

# CRITICAL: NetworkX doesn't support async operations
# Example: Convert Neo4j results to NetworkX graph synchronously

# CRITICAL: Pydantic AI agents require proper tool registration
# Example: Use @agent.tool decorator for tool functions

# CRITICAL: Windows PowerShell paths use backslashes
# Example: Use pathlib.Path for cross-platform compatibility

# CRITICAL: Neo4j Community Edition has transaction limits
# Example: Keep transactions small and focused

# CRITICAL: LangGraph state must be JSON serializable
# Example: Use Pydantic models for complex state objects
```

## Implementation Blueprint

### GitHub Copilot Workflow Integration
```yaml
# Leverage GitHub Copilot for implementation:
- Use GitHub Copilot Chat for complex logic discussions
- Leverage inline suggestions for boilerplate code
- Use Copilot agent mode (@github-pull-request_copilot-coding-agent) for full feature implementation
- Validate generated code using the validation loops below
```

### Data models and structure

Create the core data models for workplace relationship management, ensuring type safety and work-specific context.
```python
# Core models for workplace social graph entities
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class WorkRelationshipType(str, Enum):
    MANAGER = "manager"
    DIRECT_REPORT = "direct_report"
    COLLEAGUE = "colleague"
    COLLABORATOR = "collaborator"
    MENTOR = "mentor"
    MENTEE = "mentee"
    STAKEHOLDER = "stakeholder"
    VENDOR = "vendor"
    CLIENT = "client"

class CommunicationPreference(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    IN_PERSON = "in_person"
    PHONE = "phone"
    VIDEO_CALL = "video_call"

class Person(BaseModel):
    """Coworker entity in the workplace social graph."""
    id: Optional[str] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Person's full name")
    role: Optional[str] = Field(None, description="Job title or role")
    department: Optional[str] = Field(None, description="Department or team")
    email: Optional[str] = Field(None, description="Work email address")
    location: Optional[str] = Field(None, description="Office location or timezone")
    expertise_areas: List[str] = Field(default_factory=list, description="Areas of expertise")
    communication_preference: Optional[CommunicationPreference] = Field(None)
    notes: Optional[str] = Field(None, description="Personal notes about this person")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional flexible attributes")
    created_at: datetime = Field(default_factory=datetime.now)
    last_interaction: Optional[datetime] = Field(None, description="Last time you interacted")

class WorkRelationship(BaseModel):
    """Professional relationship between two people."""
    id: Optional[str] = Field(None, description="Unique identifier")
    from_person: str = Field(..., description="Source person name/id")
    to_person: str = Field(..., description="Target person name/id")
    relationship_type: WorkRelationshipType
    bidirectional: bool = Field(default=False, description="Most work relationships are hierarchical")
    strength: Optional[float] = Field(None, ge=0.0, le=1.0, description="Relationship strength/frequency")
    context: Optional[str] = Field(None, description="Context of this relationship (project, team, etc.)")
    interaction_frequency: Optional[str] = Field(None, description="How often you interact (daily, weekly, monthly)")
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

class Interaction(BaseModel):
    """Record of a specific interaction with a coworker."""
    id: Optional[str] = Field(None, description="Unique identifier")
    person_id: str = Field(..., description="Person you interacted with")
    interaction_type: str = Field(..., description="Type of interaction (meeting, email, chat, etc.)")
    topic: Optional[str] = Field(None, description="What was discussed")
    outcome: Optional[str] = Field(None, description="Result or next steps")
    date: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = Field(None, description="Additional notes about the interaction")
```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1 - Project Setup and Dependencies:
CREATE pyproject.toml updates:
  - ADD dependencies: neo4j, langgraph, click, networkx, pandas
  - ADD dev dependencies for testing and linting
  - ENSURE Windows/PowerShell compatibility

CREATE docker-compose.yml:
  - SETUP Neo4j community edition container
  - CONFIGURE ports and environment variables
  - ENABLE development-friendly settings

Task 2 - Configuration Management:
CREATE src/config/settings.py:
  - USE pydantic-settings for configuration
  - LOAD from .env files with python-dotenv
  - VALIDATE all required environment variables
  - PROVIDE sensible defaults for development

UPDATE .env.example:
  - ADD Neo4j connection settings
  - ADD LangGraph configuration
  - ADD CLI behavior settings

Task 3 - Core Data Models:
CREATE src/database/models.py:
  - DEFINE Person, WorkRelationship, and Interaction Pydantic models
  - INCLUDE work-specific fields (role, department, expertise_areas, communication_preference)
  - SUPPORT flexible attributes for additional work context
  - HANDLE hierarchical relationship logic (manager/direct_report patterns)
  - ADD interaction tracking for communication history

Task 4 - Neo4j Database Layer:
CREATE src/database/neo4j_manager.py:
  - IMPLEMENT async Neo4j driver management
  - CREATE connection pooling and session handling
  - DEFINE Cypher query builders for workplace-specific CRUD operations
  - HANDLE transaction management and error recovery
  - ADD methods for expertise-based queries and relationship traversal

CREATE src/database/migrations.py:
  - SETUP initial workplace graph schema and constraints
  - CREATE indexes for work-specific searches (department, expertise, role)
  - HANDLE database initialization and upgrades
  - ADD constraints for work hierarchy validation

Task 5 - Network Analysis Engine:
CREATE src/analysis/network_analysis.py:
  - INTEGRATE NetworkX for workplace network metrics
  - IMPLEMENT work-specific centrality measures (who's most connected, influential)
  - ADD expertise clustering and knowledge mapping
  - CONVERT Neo4j results to NetworkX format for organizational analysis
  - CREATE functions to find subject matter experts and collaboration paths

CREATE src/analysis/export_manager.py:
  - IMPLEMENT JSON export for organizational charts and team structures
  - ADD CSV export for contact lists and reporting structures
  - SUPPORT filtered exports by department, role, or expertise area
  - HANDLE privacy-conscious exports (exclude personal notes)

Task 6 - AI Agent Implementation:
CREATE src/agents/social_graph_agent.py:
  - BUILD main Pydantic AI agent for workplace relationship management
  - REGISTER tools for coworker/relationship management and interaction tracking
  - IMPLEMENT natural language query processing for work-specific questions
  - HANDLE conversation context and memory for ongoing workplace insights
  - ADD intelligence for suggesting who to contact for specific needs

CREATE src/agents/insights_agent.py:
  - CREATE specialized agent for workplace network analysis
  - INTEGRATE with network_analysis module for organizational insights
  - PROVIDE natural language explanations of team dynamics and collaboration patterns
  - SUPPORT queries like "Who should I talk to about X?" or "What's the reporting structure?"

CREATE src/agents/tools.py:
  - IMPLEMENT agent tools for workplace graph operations
  - CREATE tools for interaction logging and relationship updates
  - ADD expertise-based search and recommendation tools
  - ENSURE proper async operation and work context validation

Task 7 - CLI Interface:
CREATE src/cli/commands.py:
  - IMPLEMENT Click command groups for workplace management
  - CREATE add_coworker, add_relationship, log_interaction commands
  - ADD expertise_search, who_knows, org_chart commands for intelligent querying
  - HANDLE async operations in CLI context with work-specific validations

CREATE src/cli/chat.py:
  - BUILD interactive chat interface for workplace queries
  - INTEGRATE with social_graph_agent for natural language processing
  - SUPPORT queries like "Who should I ask about Python?" or "Show me Sarah's team"
  - HANDLE conversation history and context for ongoing workplace discussions

CREATE src/cli/utils.py:
  - CREATE output formatters for workplace data (org charts, contact info, expertise lists)
  - IMPLEMENT progress indicators for relationship mapping operations
  - ADD error message formatting for work-specific validation errors
  - SUPPORT colorized output for different relationship types and roles

Task 8 - Main Application Entry:
CREATE src/main.py:
  - SETUP Click application with command groups
  - CONFIGURE logging and error handling
  - INITIALIZE database connections
  - HANDLE graceful shutdown

Task 9 - Comprehensive Testing:
CREATE tests/conftest.py:
  - SETUP pytest fixtures for Neo4j testing
  - CREATE mock data generators
  - IMPLEMENT database cleanup utilities
  - CONFIGURE async testing support

CREATE test files for each module:
  - IMPLEMENT unit tests for all major functions
  - ADD integration tests for end-to-end workflows
  - CREATE performance tests for large graphs
  - ENSURE >80% code coverage

Task 10 - Documentation and Validation:
UPDATE README.md:
  - ADD installation and setup instructions
  - DOCUMENT CLI usage with examples
  - INCLUDE troubleshooting guide
  - PROVIDE contribution guidelines

VALIDATE complete system:
  - RUN all quality checks (ruff, mypy, tests)
  - TEST full workflow from setup to export
  - VERIFY Neo4j integration works correctly
  - CONFIRM CLI usability on Windows/PowerShell
```

### Per task pseudocode as needed added to each task

```python
# Task 4 - Neo4j Database Layer Pseudocode
class Neo4jManager:
    def __init__(self, settings: Settings):
        # PATTERN: Use async context manager for driver
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )

    async def add_coworker(self, person: Person) -> str:
        # GOTCHA: Neo4j requires proper escaping for names
        async with self.driver.session() as session:
            # PATTERN: Use parameterized queries to prevent injection
            result = await session.run(
                """CREATE (p:Person {
                    name: $name, role: $role, department: $department,
                    email: $email, expertise_areas: $expertise
                }) RETURN p.id""",
                name=person.name, role=person.role,
                department=person.department, email=person.email,
                expertise=person.expertise_areas
            )
            return result.single()["p.id"]

    async def find_experts(self, expertise_area: str) -> List[Person]:
        # CRITICAL: Work-specific query for finding subject matter experts
        async with self.driver.session() as session:
            query = """
            MATCH (p:Person)
            WHERE any(skill IN p.expertise_areas WHERE skill CONTAINS $expertise)
            RETURN p ORDER BY p.name
            """
            result = await session.run(query, expertise=expertise_area)
            return [Person(**record["p"]) for record in result]

    async def get_reporting_chain(self, person_name: str) -> List[Person]:
        # PATTERN: Traverse hierarchical relationships
        async with self.driver.session() as session:
            query = """
            MATCH path = (p:Person {name: $name})-[:REPORTS_TO*]->(manager:Person)
            RETURN nodes(path) as chain
            """
            result = await session.run(query, name=person_name)
            # Process hierarchical path results

# Task 6 - AI Agent Implementation Pseudocode
@agent.tool
async def add_coworker_tool(
    name: str, role: str = None, department: str = None,
    expertise: List[str] = None
) -> str:
    """Tool for adding a coworker to the workplace graph."""
    # PATTERN: Validate input using work-specific Pydantic models
    person = Person(
        name=name, role=role, department=department,
        expertise_areas=expertise or []
    )

    # GOTCHA: Neo4j operations must be awaited
    async with get_neo4j_session() as session:
        person_id = await session.add_coworker(person)

    return f"Coworker '{name}' added as {role} in {department}"

@agent.tool
async def find_expert_tool(expertise_area: str) -> str:
    """Tool for finding subject matter experts."""
    # PATTERN: Convert workplace queries to graph traversal
    async with get_neo4j_session() as session:
        experts = await session.find_experts(expertise_area)

    if not experts:
        return f"No experts found for {expertise_area}"

    expert_list = "\n".join([
        f"- {expert.name} ({expert.role}) - {expert.email}"
        for expert in experts
    ])
    return f"Experts in {expertise_area}:\n{expert_list}"

@agent.tool
async def who_should_i_ask_tool(question_topic: str) -> str:
    """Intelligent tool for finding the right person to ask about a topic."""
    # GOTCHA: This requires both expertise matching AND relationship context
    async with get_neo4j_session() as session:
        # Find experts in the topic
        experts = await session.find_experts(question_topic)
        # Cross-reference with your relationship strength
        accessible_experts = await session.get_accessible_contacts(experts)

    # PATTERN: Provide intelligent recommendations with context
    return format_contact_recommendations(accessible_experts, question_topic)

# Task 7 - CLI Interface Pseudocode
@click.group()
@click.pass_context
def main(ctx):
    """Workplace Relationship Manager CLI."""
    # PATTERN: Initialize shared resources with work context
    ctx.ensure_object(dict)
    ctx.obj['neo4j'] = Neo4jManager(get_settings())
    ctx.obj['agent'] = WorkplaceSocialGraphAgent()

@main.command()
@click.option('--name', required=True, help='Coworker name')
@click.option('--role', help='Job title or role')
@click.option('--department', help='Department or team')
@click.option('--expertise', multiple=True, help='Areas of expertise (can specify multiple)')
@click.pass_context
def add_coworker(ctx, name: str, role: str, department: str, expertise: tuple):
    """Add a new coworker to your workplace network."""
    # GOTCHA: Click commands need async wrapper for workplace operations
    async def _add_coworker():
        result = await ctx.obj['agent'].run(
            f"Add coworker {name}" +
            (f" with role {role}" if role else "") +
            (f" in {department}" if department else "") +
            (f" with expertise in {', '.join(expertise)}" if expertise else "")
        )
        click.echo(result)

    # PATTERN: Use asyncio.run for CLI async operations
    asyncio.run(_add_coworker())

@main.command()
@click.argument('topic')
@click.pass_context
def who_knows(ctx, topic: str):
    """Find who to ask about a specific topic."""
    async def _find_expert():
        result = await ctx.obj['agent'].run(f"Who should I ask about {topic}?")
        click.echo(result)

    asyncio.run(_find_expert())
```

### Integration Points
```yaml
DATABASE:
  - setup: "Docker Compose with Neo4j community edition"
  - constraints: "CREATE CONSTRAINT person_name_unique FOR (p:Person) REQUIRE p.name IS UNIQUE"
  - indexes: "CREATE INDEX person_lookup FOR (p:Person) ON (p.name)"

CONFIG:
  - add to: src/config/settings.py
  - pattern: "NEO4J_URI = Field(default='bolt://localhost:7687')"
  - validation: "Validate Neo4j connection on startup"

CLI:
  - entry point: src/main.py
  - pattern: "Click command groups with async support"
  - integration: "Context passing for shared resources"

AGENTS:
  - pattern: "Pydantic AI with tool registration"
  - integration: "Agent-as-tool pattern for insights agent"
  - context: "Shared Neo4j connection across tools"
```

## Validation Loop

### Level 1: Syntax & Style
```powershell
# Run these FIRST - fix any errors before proceeding (Windows PowerShell)
ruff check src/ --fix                    # Auto-fix formatting issues
mypy src/                                # Type checking
# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests for each new feature/file/function using existing test patterns
```python
# CREATE comprehensive test suite with these test cases:

# Test database models
def test_person_model_validation():
    """Person model validates workplace input correctly"""
    person = Person(
        name="Alice Johnson",
        role="Senior Developer",
        department="Engineering",
        expertise_areas=["Python", "Machine Learning"]
    )
    assert person.name == "Alice Johnson"
    assert person.role == "Senior Developer"
    assert "Python" in person.expertise_areas

    with pytest.raises(ValidationError):
        Person(name="", role="Developer")  # Empty name should fail

def test_work_relationship_model():
    """WorkRelationship handles hierarchical logic"""
    rel = WorkRelationship(
        from_person="Alice Johnson",
        to_person="Bob Smith",
        relationship_type=WorkRelationshipType.MANAGER,
        bidirectional=False,  # Manager relationships are hierarchical
        context="Engineering Team"
    )
    assert rel.bidirectional is False
    assert rel.relationship_type == WorkRelationshipType.MANAGER

# Test Neo4j operations
@pytest.mark.asyncio
async def test_neo4j_add_coworker():
    """Neo4j manager adds coworker correctly"""
    async with test_neo4j_session() as session:
        person = Person(
            name="Test Developer",
            role="Software Engineer",
            department="Engineering",
            expertise_areas=["Python", "React"]
        )
        person_id = await session.add_coworker(person)
        assert person_id is not None

        # Verify person exists in database with work attributes
        result = await session.get_person_by_name("Test Developer")
        assert result.name == "Test Developer"
        assert result.role == "Software Engineer"
        assert "Python" in result.expertise_areas

@pytest.mark.asyncio
async def test_find_experts():
    """Neo4j manager finds subject matter experts"""
    async with test_neo4j_session() as session:
        # Add some test coworkers with expertise
        await session.add_coworker(Person(
            name="Python Expert", expertise_areas=["Python", "Django"]
        ))
        await session.add_coworker(Person(
            name="ML Specialist", expertise_areas=["Machine Learning", "Python"]
        ))

        experts = await session.find_experts("Python")
        assert len(experts) == 2
        expert_names = [expert.name for expert in experts]
        assert "Python Expert" in expert_names
        assert "ML Specialist" in expert_names

# Test CLI commands
def test_add_coworker_command():
    """CLI add_coworker command works"""
    runner = CliRunner()
    result = runner.invoke(add_coworker, [
        '--name', 'Alice Johnson',
        '--role', 'Senior Developer',
        '--department', 'Engineering',
        '--expertise', 'Python',
        '--expertise', 'Machine Learning'
    ])
    assert result.exit_code == 0
    assert "Alice Johnson" in result.output
    assert "Senior Developer" in result.output

def test_who_knows_command():
    """CLI who_knows command finds experts"""
    runner = CliRunner()
    result = runner.invoke(who_knows, ['Python'])
    assert result.exit_code == 0
    # Should return relevant experts or "No experts found"

# Test workplace network analysis
def test_expertise_clustering():
    """Network analysis clusters people by expertise correctly"""
    # Create test workplace graph
    test_graph = create_test_workplace_graph()
    clusters = cluster_by_expertise(test_graph, "Python")
    assert isinstance(clusters, dict)
    assert all(isinstance(people, list) for people in clusters.values())

# Test agent tools
@pytest.mark.asyncio
async def test_agent_add_coworker_tool():
    """Agent tool adds coworker correctly"""
    agent = WorkplaceSocialGraphAgent()
    result = await agent.run(
        "Add Alice Johnson as Senior Developer in Engineering with Python expertise"
    )
    assert "Alice Johnson" in result
    assert "added" in result.lower()

@pytest.mark.asyncio
async def test_agent_find_expert_tool():
    """Agent tool finds experts correctly"""
    agent = WorkplaceSocialGraphAgent()
    result = await agent.run("Who should I ask about Python development?")
    assert "expert" in result.lower() or "no experts found" in result.lower()
```

```powershell
# Run and iterate until passing (Windows PowerShell):
uv run pytest tests/ -v --cov=src --cov-report=term-missing
# Target: >80% coverage. If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test
```powershell
# Start Neo4j database (Windows PowerShell)
docker-compose up -d neo4j

# Wait for database to be ready
Start-Sleep -Seconds 10

# Run the full application (Windows PowerShell)
uv run python -m src.main

# Test CLI commands interactively
uv run python -m src.main add-coworker --name "Alice Johnson" --role "Senior Developer" --department "Engineering" --expertise "Python" --expertise "Machine Learning"
uv run python -m src.main add-coworker --name "Bob Smith" --role "Product Manager" --department "Product"
uv run python -m src.main add-relationship --from "Alice Johnson" --to "Bob Smith" --type "collaborator" --context "Q2 Planning Project"
uv run python -m src.main who-knows "Python machine learning"
uv run python -m src.main org-chart --department "Engineering"

# Test chat interface for natural language queries
uv run python -m src.main chat
# Expected: Interactive prompt where you can ask questions like:
# "Who should I talk to about the API redesign?"
# "Show me everyone in Alice's team"
# "Who are my direct reports?"

# Test export functionality for workplace data
uv run python -m src.main export --format json --filter department=Engineering --output engineering_team.json
uv run python -m src.main export --format csv --type contacts --output coworker_contacts.csv

# Cleanup
docker-compose down
```

## Final validation Checklist
- [ ] All tests pass: `uv run pytest tests/ -v --cov=src --cov-report=term-missing`
- [ ] No linting errors: `ruff check src/`
- [ ] No type errors: `mypy src/`
- [ ] Neo4j integration works: Docker compose up and connection test
- [ ] CLI commands work: Manual testing of add_coworker, add_relationship, who_knows, org_chart
- [ ] Chat interface responds: Interactive workplace queries like "Who should I ask about X?"
- [ ] Export functions work: JSON/CSV generation for workplace data (org charts, contact lists)
- [ ] Intelligent queries work: Finding experts, relationship traversal, collaboration suggestions
- [ ] Error cases handled gracefully: Invalid inputs, connection failures, missing relationships
- [ ] Privacy preserved: Local-only operation, no external data transmission
- [ ] Documentation complete: README with workplace-specific setup and usage examples

---

## Anti-Patterns to Avoid
- ❌ Don't use sync operations with Neo4j driver - always use async
- ❌ Don't skip Neo4j transaction management - use proper session handling
- ❌ Don't ignore NetworkX synchronous nature - convert data properly
- ❌ Don't hardcode Neo4j queries - use parameterized queries
- ❌ Don't mix Click sync/async patterns - use consistent async approach
- ❌ Don't create massive graphs in memory - use streaming for large datasets
- ❌ Don't skip input validation - use Pydantic models throughout
- ❌ Don't ignore Windows path differences - use pathlib.Path
- ❌ Don't create circular imports - organize dependencies properly
- ❌ Don't skip database cleanup in tests - use proper fixtures

## Quality Score Assessment
**Confidence Level: 8/10**

This PRP provides comprehensive context including:
✅ Complete library documentation references with specific URLs
✅ Detailed implementation patterns from codebase analysis
✅ Thorough gotchas and library-specific quirks
✅ Step-by-step implementation blueprint with pseudocode
✅ Executable validation loops with PowerShell commands
✅ Complete test strategy with >80% coverage target
✅ Windows/PowerShell compatibility throughout
✅ GitHub Copilot integration guidelines

Areas for potential iteration:
- LangGraph integration may require additional research during implementation
- Neo4j performance optimization might need tuning based on data size
- CLI UX might benefit from user feedback during development

The PRP is structured for one-pass implementation success using GitHub Copilot agent mode with comprehensive self-validation capabilities.
