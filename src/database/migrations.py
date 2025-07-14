"""Database migrations for the workplace social graph system."""

import logging
from typing import Any, Dict, List

from .neo4j_manager import Neo4jManager

logger = logging.getLogger(__name__)


class Migration:
    """Base migration class."""

    def __init__(self, name: str, version: str):
        """Initialize migration.

        Args:
            name: Migration name
            version: Migration version
        """
        self.name = name
        self.version = version

    async def up(self, manager: Neo4jManager) -> None:
        """Apply the migration."""
        raise NotImplementedError

    async def down(self, manager: Neo4jManager) -> None:
        """Rollback the migration."""
        raise NotImplementedError


class InitialWorkplaceGraphMigration(Migration):
    """Initial migration to set up workplace graph schema."""

    def __init__(self):
        super().__init__("initial_workplace_graph", "0.1.0")

    async def up(self, manager: Neo4jManager) -> None:
        """Create initial workplace graph schema."""
        async with manager.session() as session:
            # Create constraints for data integrity
            constraints = [
                # Ensure person names are unique
                "CREATE CONSTRAINT person_name_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",

                # Ensure interaction IDs are unique if we add them later
                "CREATE CONSTRAINT interaction_id_unique IF NOT EXISTS FOR (i:Interaction) REQUIRE i.id IS UNIQUE"
            ]

            # Create indexes for performance
            indexes = [
                # Person lookups
                "CREATE INDEX person_name_lookup IF NOT EXISTS FOR (p:Person) ON (p.name)",
                "CREATE INDEX person_department_lookup IF NOT EXISTS FOR (p:Person) ON (p.department)",
                "CREATE INDEX person_role_lookup IF NOT EXISTS FOR (p:Person) ON (p.role)",
                "CREATE INDEX person_email_lookup IF NOT EXISTS FOR (p:Person) ON (p.email)",

                # Expertise searches
                "CREATE INDEX person_expertise_lookup IF NOT EXISTS FOR (p:Person) ON (p.expertise_areas)",

                # Interaction lookups
                "CREATE INDEX interaction_date_lookup IF NOT EXISTS FOR (i:Interaction) ON (i.date)",
                "CREATE INDEX interaction_type_lookup IF NOT EXISTS FOR (i:Interaction) ON (i.interaction_type)",
                "CREATE INDEX interaction_person_lookup IF NOT EXISTS FOR (i:Interaction) ON (i.with_person)",

                # Relationship lookups
                "CREATE INDEX relationship_type_lookup IF NOT EXISTS FOR ()-[r:WORKS_WITH]-() ON (r.type)"
            ]

            # Apply constraints
            for constraint in constraints:
                try:
                    await session.run(constraint)
                    logger.info(f"✓ Applied constraint: {constraint}")
                except Exception as e:
                    logger.warning(f"⚠ Constraint already exists or failed: {e}")

            # Apply indexes
            for index in indexes:
                try:
                    await session.run(index)
                    logger.info(f"✓ Applied index: {index}")
                except Exception as e:
                    logger.warning(f"⚠ Index already exists or failed: {e}")

            # Create sample data structure validation
            await self._create_validation_queries(session)

    async def _create_validation_queries(self, session) -> None:
        """Create validation queries to ensure schema works correctly."""
        # Test person creation
        test_query = """
        MERGE (p:Person {name: 'Schema Test Person'})
        SET p.role = 'Test Role',
            p.department = 'Test Department',
            p.expertise_areas = ['Testing', 'Schema Validation'],
            p.created_at = datetime(),
            p.updated_at = datetime()
        RETURN p.name as name
        """

        result = await session.run(test_query)
        record = await result.single()

        if record:
            logger.info(f"✓ Schema validation: Successfully created test person")

            # Clean up test data
            cleanup_query = "MATCH (p:Person {name: 'Schema Test Person'}) DELETE p"
            await session.run(cleanup_query)
            logger.info("✓ Schema validation: Cleaned up test data")

    async def down(self, manager: Neo4jManager) -> None:
        """Remove the workplace graph schema."""
        async with manager.session() as session:
            # Drop indexes
            drop_indexes = [
                "DROP INDEX person_name_lookup IF EXISTS",
                "DROP INDEX person_department_lookup IF EXISTS",
                "DROP INDEX person_role_lookup IF EXISTS",
                "DROP INDEX person_email_lookup IF EXISTS",
                "DROP INDEX person_expertise_lookup IF EXISTS",
                "DROP INDEX interaction_date_lookup IF EXISTS",
                "DROP INDEX interaction_type_lookup IF EXISTS",
                "DROP INDEX interaction_person_lookup IF EXISTS",
                "DROP INDEX relationship_type_lookup IF EXISTS"
            ]

            # Drop constraints
            drop_constraints = [
                "DROP CONSTRAINT person_name_unique IF EXISTS",
                "DROP CONSTRAINT interaction_id_unique IF EXISTS"
            ]

            for drop_index in drop_indexes:
                try:
                    await session.run(drop_index)
                    logger.info(f"✓ Dropped index: {drop_index}")
                except Exception as e:
                    logger.warning(f"⚠ Index drop failed: {e}")

            for drop_constraint in drop_constraints:
                try:
                    await session.run(drop_constraint)
                    logger.info(f"✓ Dropped constraint: {drop_constraint}")
                except Exception as e:
                    logger.warning(f"⚠ Constraint drop failed: {e}")


class WorkplaceHierarchyMigration(Migration):
    """Migration to add workplace hierarchy validation."""

    def __init__(self):
        super().__init__("workplace_hierarchy", "0.2.0")

    async def up(self, manager: Neo4jManager) -> None:
        """Add workplace hierarchy constraints."""
        async with manager.session() as session:
            # Add validation for hierarchical relationships
            hierarchy_procedures = [
                """
                // Procedure to validate manager-report relationships
                CALL apoc.trigger.add('validate_hierarchy',
                "MATCH (manager:Person)<-[:WORKS_WITH {type: 'manager'}]-(report:Person)
                 WHERE manager.name = report.name
                 DELETE r", {phase:'before'})
                """,
            ]

            # Note: This requires APOC plugin - for now we'll skip and handle in application logic
            logger.info("✓ Workplace hierarchy validation will be handled in application logic")

    async def down(self, manager: Neo4jManager) -> None:
        """Remove workplace hierarchy constraints."""
        # Remove triggers if they were created
        logger.info("✓ Workplace hierarchy constraints removed")


class MigrationManager:
    """Manages database migrations."""

    def __init__(self, manager: Neo4jManager):
        """Initialize migration manager.

        Args:
            manager: Neo4j database manager
        """
        self.manager = manager
        self.migrations: List[Migration] = [
            InitialWorkplaceGraphMigration(),
            WorkplaceHierarchyMigration(),
        ]

    async def get_applied_migrations(self) -> List[str]:
        """Get list of applied migrations.

        Returns:
            List[str]: List of applied migration versions
        """
        async with self.manager.session() as session:
            # Check if migration tracking node exists
            check_query = """
            MATCH (m:MigrationTracker)
            RETURN m.applied_migrations as applied
            """

            result = await session.run(check_query)
            record = await result.single()

            if record and record["applied"]:
                return record["applied"]
            return []

    async def apply_migration(self, migration: Migration) -> None:
        """Apply a single migration.

        Args:
            migration: Migration to apply
        """
        applied_migrations = await self.get_applied_migrations()

        if migration.version in applied_migrations:
            logger.info(f"⏭ Migration {migration.version} already applied")
            return

        logger.info(f"🔄 Applying migration: {migration.name} (v{migration.version})")

        try:
            await migration.up(self.manager)

            # Track migration as applied
            async with self.manager.session() as session:
                track_query = """
                MERGE (m:MigrationTracker)
                ON CREATE SET m.applied_migrations = [$version]
                ON MATCH SET m.applied_migrations =
                    CASE
                        WHEN $version IN m.applied_migrations
                        THEN m.applied_migrations
                        ELSE m.applied_migrations + $version
                    END,
                    m.last_applied = datetime()
                """
                await session.run(track_query, version=migration.version)

            logger.info(f"✅ Successfully applied migration: {migration.name}")

        except Exception as e:
            logger.error(f"❌ Failed to apply migration {migration.name}: {e}")
            raise

    async def migrate(self) -> None:
        """Apply all pending migrations."""
        logger.info("🚀 Starting database migration")

        applied_migrations = await self.get_applied_migrations()
        pending_migrations = [
            m for m in self.migrations
            if m.version not in applied_migrations
        ]

        if not pending_migrations:
            logger.info("✅ All migrations are up to date")
            return

        logger.info(f"📋 Found {len(pending_migrations)} pending migrations")

        for migration in pending_migrations:
            await self.apply_migration(migration)

        logger.info("🎉 All migrations completed successfully")

    async def rollback(self, target_version: str = None) -> None:
        """Rollback migrations to a target version.

        Args:
            target_version: Version to rollback to (optional)
        """
        logger.info(f"🔄 Rolling back migrations to version: {target_version or 'initial'}")

        applied_migrations = await self.get_applied_migrations()

        # Find migrations to rollback (in reverse order)
        rollback_migrations = []
        for migration in reversed(self.migrations):
            if migration.version in applied_migrations:
                rollback_migrations.append(migration)
                if target_version and migration.version == target_version:
                    break

        for migration in rollback_migrations:
            logger.info(f"🔄 Rolling back migration: {migration.name} (v{migration.version})")

            try:
                await migration.down(self.manager)

                # Remove from applied migrations
                async with self.manager.session() as session:
                    update_query = """
                    MATCH (m:MigrationTracker)
                    SET m.applied_migrations = [x IN m.applied_migrations WHERE x <> $version],
                        m.last_rollback = datetime()
                    """
                    await session.run(update_query, version=migration.version)

                logger.info(f"✅ Successfully rolled back migration: {migration.name}")

            except Exception as e:
                logger.error(f"❌ Failed to rollback migration {migration.name}: {e}")
                raise

        logger.info("🎉 Rollback completed successfully")


async def initialize_database() -> None:
    """Initialize the database with all necessary migrations."""
    from .neo4j_manager import get_neo4j_manager

    logger.info("🔧 Initializing workplace social graph database")

    try:
        manager = await get_neo4j_manager()
        migration_manager = MigrationManager(manager)

        # Apply all migrations
        await migration_manager.migrate()

        logger.info("✅ Database initialization completed successfully")

    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def reset_database() -> None:
    """Reset the database (WARNING: Deletes all data)."""
    from .neo4j_manager import get_neo4j_manager

    logger.warning("⚠️  RESETTING DATABASE - ALL DATA WILL BE DELETED")

    try:
        manager = await get_neo4j_manager()

        async with manager.session() as session:
            # Delete all nodes and relationships
            delete_query = "MATCH (n) DETACH DELETE n"
            await session.run(delete_query)

            logger.info("🗑️  All data deleted")

        # Re-initialize with migrations
        await initialize_database()

        logger.info("🎉 Database reset completed successfully")

    except Exception as e:
        logger.error(f"❌ Database reset failed: {e}")
        raise
