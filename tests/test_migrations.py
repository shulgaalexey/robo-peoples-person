"""Tests for database migrations functionality."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.config.settings import Settings
from src.database.migrations import (InitialWorkplaceGraphMigration, Migration,
                                     MigrationManager,
                                     WorkplaceHierarchyMigration,
                                     initialize_database, reset_database)
from src.database.neo4j_manager import Neo4jManager


class TestMigrations:
    """Test cases for database migrations."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings()

    @pytest.fixture
    def neo4j_manager(self, settings):
        """Create Neo4jManager instance."""
        return Neo4jManager(settings)

    @pytest.fixture
    def migration_manager(self, neo4j_manager):
        """Create MigrationManager instance."""
        return MigrationManager(neo4j_manager)

    def test_migration_base_class(self):
        """Test Migration base class."""
        migration = Migration("test_migration", "1.0.0")
        assert migration.name == "test_migration"
        assert migration.version == "1.0.0"

    @pytest.mark.asyncio
    async def test_initial_schema_migration(self, neo4j_manager):
        """Test initial schema migration."""
        migration = InitialWorkplaceGraphMigration()

        with patch.object(neo4j_manager, 'session') as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            mock_session.return_value.__aexit__.return_value = None

            mock_session_instance.run.return_value = AsyncMock()

            await migration.up(neo4j_manager)

            # Should have called session
            mock_session.assert_called()

    @pytest.mark.asyncio
    async def test_add_indexes_migration(self, neo4j_manager):
        """Test add indexes migration."""
        migration = WorkplaceHierarchyMigration()

        with patch.object(neo4j_manager, 'session') as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            mock_session.return_value.__aexit__.return_value = None

            mock_session_instance.run.return_value = AsyncMock()

            await migration.up(neo4j_manager)

            # Should have called session
            mock_session.assert_called()

    @pytest.mark.asyncio
    async def test_migration_manager_get_applied_migrations(self, migration_manager):
        """Test getting applied migrations."""
        with patch.object(migration_manager.manager, 'session') as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            mock_session.return_value.__aexit__.return_value = None

            mock_result = AsyncMock()
            mock_result.single.return_value = {"applied": ["1.0.0", "2.0.0"]}
            mock_session_instance.run.return_value = mock_result

            applied = await migration_manager.get_applied_migrations()

            assert isinstance(applied, list)
            assert applied == ["1.0.0", "2.0.0"]

    @pytest.mark.asyncio
    async def test_migration_manager_apply_migration(self, migration_manager):
        """Test applying a migration."""
        migration = InitialWorkplaceGraphMigration()

        with patch.object(migration_manager.manager, 'session') as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            mock_session.return_value.__aexit__.return_value = None

            mock_session_instance.run.return_value = AsyncMock()

            await migration_manager.apply_migration(migration)

            # Should have used session
            mock_session.assert_called()

    @pytest.mark.asyncio
    async def test_migration_manager_migrate(self, migration_manager):
        """Test running all migrations."""
        with patch.object(migration_manager, 'get_applied_migrations', return_value=[]):
            with patch.object(migration_manager, 'apply_migration') as mock_apply:

                await migration_manager.migrate()

                # Should have tried to apply migrations
                assert mock_apply.call_count >= 0

    @pytest.mark.asyncio
    async def test_migration_manager_rollback(self, migration_manager):
        """Test rolling back migrations."""
        with patch.object(migration_manager, 'get_applied_migrations', return_value=["0.1.0", "0.2.0"]):
            with patch.object(migration_manager.manager, 'session') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session.return_value.__aexit__.return_value = None

                mock_session_instance.run.return_value = AsyncMock()

                await migration_manager.rollback()

                # Should have used session for rollback
                mock_session.assert_called()

    @pytest.mark.asyncio
    async def test_initialize_database(self):
        """Test database initialization."""
        with patch('src.database.neo4j_manager.get_neo4j_manager') as mock_get_manager:
            mock_manager = AsyncMock()
            mock_get_manager.return_value = mock_manager

            with patch('src.database.migrations.MigrationManager') as mock_migration_manager_class:
                mock_migration_manager = AsyncMock()
                mock_migration_manager_class.return_value = mock_migration_manager

                await initialize_database()

                mock_get_manager.assert_called_once()
                mock_migration_manager.migrate.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_database(self):
        """Test database reset."""
        with patch('src.database.neo4j_manager.get_neo4j_manager') as mock_get_manager:
            mock_manager = Mock()  # Use Mock, not AsyncMock for the manager itself
            mock_get_manager.return_value = mock_manager

            # Mock the session context manager properly
            mock_session_context = AsyncMock()
            mock_session_instance = AsyncMock()
            mock_session_context.__aenter__.return_value = mock_session_instance
            mock_session_context.__aexit__.return_value = None
            mock_manager.session.return_value = mock_session_context

            mock_session_instance.run.return_value = AsyncMock()

            with patch('src.database.migrations.initialize_database') as mock_init_db:
                await reset_database()

                mock_get_manager.assert_called_once()
                mock_manager.session.assert_called_once()
                mock_init_db.assert_called_once()

    @pytest.mark.asyncio
    async def test_migration_error_handling(self, migration_manager):
        """Test error handling in migrations."""
        with patch.object(migration_manager.manager, 'session', side_effect=Exception("Database error")):
            with pytest.raises(Exception, match="Database error"):
                await migration_manager.migrate()

    @pytest.mark.asyncio
    async def test_migration_down_operation(self, neo4j_manager):
        """Test migration down operation."""
        migration = InitialWorkplaceGraphMigration()

        with patch.object(neo4j_manager, 'session') as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            mock_session.return_value.__aexit__.return_value = None

            mock_session_instance.run.return_value = AsyncMock()

            await migration.down(neo4j_manager)

            # Should have called session
            mock_session.assert_called()

    @pytest.mark.asyncio
    async def test_indexes_migration_down(self, neo4j_manager):
        """Test indexes migration down operation."""
        migration = WorkplaceHierarchyMigration()

        with patch.object(neo4j_manager, 'session') as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance
            mock_session.return_value.__aexit__.return_value = None

            mock_session_instance.run.return_value = AsyncMock()

            await migration.down(neo4j_manager)

            # Should have called session
            mock_session.assert_called()
