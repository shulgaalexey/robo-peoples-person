"""Neo4j database manager for workplace social graph operations."""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession
from neo4j.exceptions import AuthError, ServiceUnavailable

from ..config.settings import Settings
from .models import Interaction, Person, WorkRelationship, WorkRelationshipType

logger = logging.getLogger(__name__)


class Neo4jManager:
    """Async Neo4j database manager for workplace graph operations."""

    def __init__(self, settings: Settings = None, uri: str = None, user: str = None, password: str = None):
        """Initialize Neo4j manager.

        Args:
            settings: Settings instance with database configuration
            uri: Neo4j connection URI (overrides settings)
            user: Neo4j username (overrides settings)
            password: Neo4j password (overrides settings)
        """
        self.settings = settings or Settings()
        self.uri = uri or self.settings.neo4j_uri
        self.user = user or self.settings.neo4j_user
        self.password = password or self.settings.neo4j_password
        self.database = self.settings.neo4j_database
        self._driver: Optional[AsyncDriver] = None

    async def connect(self) -> None:
        """Establish connection to Neo4j database."""
        try:
            self._driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test the connection with timeout
            await asyncio.wait_for(self._driver.verify_connectivity(), timeout=5.0)
            logger.info("Successfully connected to Neo4j database")
        except asyncio.TimeoutError:
            logger.error("Neo4j connection timed out after 5 seconds")
            raise
        except (ServiceUnavailable, AuthError) as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    async def close(self) -> None:
        """Close the database connection."""
        if self._driver:
            await self._driver.close()
            logger.info("Neo4j connection closed")

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        """Get an async Neo4j session context manager.

        Yields:
            AsyncSession: Neo4j session for database operations
        """
        if not self._driver:
            await self.connect()

        session = self._driver.session(database=self.database)
        try:
            yield session
        finally:
            await session.close()

    async def add_coworker(self, person: Person) -> str:
        """Add a coworker to the workplace graph.

        Args:
            person: Person model instance

        Returns:
            str: The person's name (used as ID)
        """
        async with self.session() as session:
            query = """
            MERGE (p:Person {name: $name})
            SET p.email = $email,
                p.phone = $phone,
                p.role = $role,
                p.department = $department,
                p.manager = $manager,
                p.expertise_areas = $expertise_areas,
                p.communication_preference = $communication_preference,
                p.availability = $availability,
                p.timezone = $timezone,
                p.last_interaction = $last_interaction,
                p.interaction_frequency = $interaction_frequency,
                p.notes = $notes,
                p.attributes = $attributes,
                p.created_at = $created_at,
                p.updated_at = $updated_at
            RETURN p.name as name
            """

            result = await session.run(query, **person.model_dump())
            record = await result.single()
            return record["name"] if record else person.name

    async def get_person_by_name(self, name: str) -> Optional[Person]:
        """Get a person by name.

        Args:
            name: Person's name

        Returns:
            Person: Person model instance or None if not found
        """
        async with self.session() as session:
            query = """
            MATCH (p:Person {name: $name})
            RETURN p
            """

            result = await session.run(query, name=name)
            record = await result.single()

            if record:
                person_data = record["p"]
                return Person(**person_data)
            return None

    async def add_relationship(self, relationship: WorkRelationship) -> bool:
        """Add a workplace relationship between two people.

        Args:
            relationship: WorkRelationship model instance

        Returns:
            bool: True if successful
        """
        async with self.session() as session:
            # First ensure both people exist
            await self._ensure_person_exists(session, relationship.from_person)
            await self._ensure_person_exists(session, relationship.to_person)

            # Create the relationship
            query = """
            MATCH (from:Person {name: $from_person})
            MATCH (to:Person {name: $to_person})
            MERGE (from)-[r:WORKS_WITH {type: $relationship_type}]->(to)
            SET r.bidirectional = $bidirectional,
                r.strength = $strength,
                r.context = $context,
                r.created_at = $created_at,
                r.updated_at = $updated_at,
                r.notes = $notes
            RETURN r
            """

            await session.run(query, **relationship.model_dump())

            # If bidirectional, create reverse relationship
            if relationship.bidirectional:
                reverse_query = """
                MATCH (from:Person {name: $to_person})
                MATCH (to:Person {name: $from_person})
                MERGE (from)-[r:WORKS_WITH {type: $relationship_type}]->(to)
                SET r.bidirectional = $bidirectional,
                    r.strength = $strength,
                    r.context = $context,
                    r.created_at = $created_at,
                    r.updated_at = $updated_at,
                    r.notes = $notes
                RETURN r
                """
                await session.run(reverse_query, **relationship.model_dump())

            return True

    async def add_interaction(self, interaction: Interaction) -> bool:
        """Add an interaction record.

        Args:
            interaction: Interaction model instance

        Returns:
            bool: True if successful
        """
        async with self.session() as session:
            # Ensure person exists
            await self._ensure_person_exists(session, interaction.with_person)

            # Add interaction
            query = """
            MATCH (p:Person {name: $with_person})
            CREATE (i:Interaction {
                with_person: $with_person,
                interaction_type: $interaction_type,
                topic: $topic,
                outcome: $outcome,
                duration_minutes: $duration_minutes,
                project: $project,
                location: $location,
                participants: $participants,
                date: $date,
                notes: $notes,
                follow_up_required: $follow_up_required,
                follow_up_date: $follow_up_date
            })
            CREATE (p)-[:HAD_INTERACTION]->(i)
            RETURN i
            """

            await session.run(query, **interaction.model_dump())

            # Update person's last interaction
            update_query = """
            MATCH (p:Person {name: $with_person})
            SET p.last_interaction = $date,
                p.updated_at = $date
            """
            await session.run(update_query,
                            with_person=interaction.with_person,
                            date=interaction.date)

            return True

    async def find_experts(self, expertise_area: str, department: str = None) -> List[Person]:
        """Find subject matter experts by expertise area.

        Args:
            expertise_area: Area of expertise to search for
            department: Optional department filter

        Returns:
            List[Person]: List of expert persons
        """
        async with self.session() as session:
            query = """
            MATCH (p:Person)
            WHERE any(skill IN p.expertise_areas WHERE skill CONTAINS $expertise)
            """

            params = {"expertise": expertise_area}

            if department:
                query += " AND p.department = $department"
                params["department"] = department

            query += " RETURN p ORDER BY p.name"

            result = await session.run(query, **params)
            experts = []

            async for record in result:
                person_data = record["p"]
                experts.append(Person(**person_data))

            return experts

    async def get_reporting_chain(self, person_name: str) -> List[Person]:
        """Get the reporting chain for a person (all managers up the hierarchy).

        Args:
            person_name: Name of the person

        Returns:
            List[Person]: List of managers in reporting chain
        """
        async with self.session() as session:
            query = """
            MATCH path = (p:Person {name: $name})-[:WORKS_WITH {type: 'manager'}*]->(manager:Person)
            RETURN nodes(path) as chain
            """

            result = await session.run(query, name=person_name)
            record = await result.single()

            if record:
                chain_nodes = record["chain"]
                return [Person(**node) for node in chain_nodes[1:]]  # Skip self

            return []

    async def get_direct_reports(self, person_name: str) -> List[Person]:
        """Get direct reports for a person.

        Args:
            person_name: Name of the manager

        Returns:
            List[Person]: List of direct reports
        """
        async with self.session() as session:
            query = """
            MATCH (manager:Person {name: $name})<-[:WORKS_WITH {type: 'manager'}]-(report:Person)
            RETURN report
            ORDER BY report.name
            """

            result = await session.run(query, name=person_name)
            reports = []

            async for record in result:
                person_data = record["report"]
                reports.append(Person(**person_data))

            return reports

    async def get_collaboration_path(self, from_person: str, to_person: str) -> List[str]:
        """Find the shortest collaboration path between two people.

        Args:
            from_person: Starting person name
            to_person: Target person name

        Returns:
            List[str]: List of person names in the path
        """
        async with self.session() as session:
            query = """
            MATCH path = shortestPath((from:Person {name: $from_person})-[:WORKS_WITH*]-(to:Person {name: $to_person}))
            RETURN [node in nodes(path) | node.name] as path
            """

            result = await session.run(query, from_person=from_person, to_person=to_person)
            record = await result.single()

            return record["path"] if record else []

    async def get_team_members(self, department: str = None, manager: str = None) -> List[Person]:
        """Get team members by department or manager.

        Args:
            department: Department name
            manager: Manager name

        Returns:
            List[Person]: List of team members
        """
        async with self.session() as session:
            query = "MATCH (p:Person)"
            params = {}

            if department:
                query += " WHERE p.department = $department"
                params["department"] = department
            elif manager:
                query += " WHERE p.manager = $manager"
                params["manager"] = manager

            query += " RETURN p ORDER BY p.name"

            result = await session.run(query, **params)
            members = []

            async for record in result:
                person_data = record["p"]
                members.append(Person(**person_data))

            return members

    async def get_recent_interactions(self, person_name: str = None, days: int = 30) -> List[Interaction]:
        """Get recent interactions, optionally filtered by person.

        Args:
            person_name: Optional person name filter
            days: Number of days to look back

        Returns:
            List[Interaction]: List of recent interactions
        """
        async with self.session() as session:
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
            interactions = []

            async for record in result:
                interaction_data = record["i"]
                interactions.append(Interaction(**interaction_data))

            return interactions

    async def _ensure_person_exists(self, session: AsyncSession, person_name: str) -> None:
        """Ensure a person exists in the database, create if not.

        Args:
            session: Neo4j session
            person_name: Name of the person
        """
        query = """
        MERGE (p:Person {name: $name})
        ON CREATE SET p.created_at = datetime(),
                     p.updated_at = datetime()
        """
        await session.run(query, name=person_name)

    async def initialize_schema(self) -> None:
        """Initialize database schema with constraints and indexes."""
        async with self.session() as session:
            # Create constraints
            constraints = [
                "CREATE CONSTRAINT person_name_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE"
            ]

            # Create indexes
            indexes = [
                "CREATE INDEX person_lookup IF NOT EXISTS FOR (p:Person) ON (p.name)",
                "CREATE INDEX person_department IF NOT EXISTS FOR (p:Person) ON (p.department)",
                "CREATE INDEX person_role IF NOT EXISTS FOR (p:Person) ON (p.role)",
                "CREATE INDEX interaction_date IF NOT EXISTS FOR (i:Interaction) ON (i.date)",
                "CREATE INDEX interaction_type IF NOT EXISTS FOR (i:Interaction) ON (i.interaction_type)"
            ]

            for constraint in constraints:
                try:
                    await session.run(constraint)
                    logger.info(f"Created constraint: {constraint}")
                except Exception as e:
                    logger.warning(f"Constraint already exists or failed: {e}")

            for index in indexes:
                try:
                    await session.run(index)
                    logger.info(f"Created index: {index}")
                except Exception as e:
                    logger.warning(f"Index already exists or failed: {e}")


# Global Neo4j manager instance
_neo4j_manager: Optional[Neo4jManager] = None


async def get_neo4j_manager() -> Neo4jManager:
    """Get the global Neo4j manager instance.

    Returns:
        Neo4jManager: Global Neo4j manager
    """
    global _neo4j_manager
    if not _neo4j_manager:
        _neo4j_manager = Neo4jManager()
        await _neo4j_manager.connect()
    return _neo4j_manager


@asynccontextmanager
async def get_neo4j_session():
    """Get a Neo4j session context manager.

    Yields:
        Neo4jManager: Neo4j manager with active session
    """
    manager = await get_neo4j_manager()
    async with manager.session() as session:
        yield manager
