"""Test configuration settings."""

import os
from unittest.mock import patch

import pytest

from src.config.settings import Settings


def test_settings_defaults():
    """Test default configuration values."""
    settings = Settings()

    assert settings.neo4j_uri == "bolt://localhost:7687"
    assert settings.neo4j_user == "neo4j"
    assert settings.neo4j_password == "password123"
    assert settings.neo4j_database == "neo4j"
    assert settings.app_name == "Robo People's Person"
    assert settings.app_version == "0.1.0"
    assert settings.debug == False
    assert settings.cli_output_format == "table"
    assert settings.cli_color_output == True
    assert settings.agent_memory_size == 1000
    assert settings.agent_timeout == 30
    assert settings.max_graph_size == 10000
    assert settings.export_batch_size == 1000


def test_database_url_property():
    """Test database URL construction."""
    settings = Settings()
    url = settings.database_url

    assert settings.neo4j_user in url
    assert settings.neo4j_password in url
    assert "localhost:7687" in url


def test_database_url_without_credentials():
    """Test database URL with custom credentials."""
    settings = Settings(
        neo4j_uri="bolt://example.com:7687",
        neo4j_user="testuser",
        neo4j_password="testpass"
    )
    url = settings.database_url

    assert "testuser:testpass@example.com:7687" in url


def test_settings_from_env():
    """Test settings loading from environment variables."""
    with patch.dict(os.environ, {
        'NEO4J_URI': 'bolt://test:7687',
        'NEO4J_USER': 'testuser',
        'NEO4J_PASSWORD': 'testpass',
        'NEO4J_DATABASE': 'testdb',
        'DEBUG': 'true',
        'AGENT_MEMORY_SIZE': '2000',
        'AGENT_TIMEOUT': '60'
    }, clear=True):
        settings = Settings()

        assert settings.neo4j_uri == 'bolt://test:7687'
        assert settings.neo4j_user == 'testuser'
        assert settings.neo4j_password == 'testpass'
        assert settings.neo4j_database == 'testdb'
        assert settings.debug == True
        assert settings.agent_memory_size == 2000
        assert settings.agent_timeout == 60


def test_settings_from_env_partial():
    """Test settings with partial environment variables."""
    with patch.dict(os.environ, {
        'NEO4J_URI': 'bolt://test:7687',
        'NEO4J_USER': 'testuser',
        # NEO4J_PASSWORD not set - should use default
    }, clear=True):
        settings = Settings()

        assert settings.neo4j_uri == 'bolt://test:7687'
        assert settings.neo4j_user == 'testuser'
        assert settings.neo4j_password == 'password123'  # default value


def test_settings_validation():
    """Test settings validation."""
    # Test that required fields are handled properly
    settings = Settings()

    # All fields should have defaults or be optional
    assert settings.neo4j_uri is not None
    assert settings.neo4j_user is not None
    assert settings.neo4j_password is not None


def test_settings_model_config():
    """Test settings model configuration."""
    settings = Settings()

    # Should have proper pydantic configuration
    assert hasattr(settings, 'model_fields')
    assert 'neo4j_uri' in settings.model_fields
    assert 'neo4j_user' in settings.model_fields
    assert 'neo4j_password' in settings.model_fields


def test_settings_custom_values():
    """Test settings with custom values."""
    settings = Settings(
        neo4j_uri="bolt://custom:7687",
        neo4j_user="custom_user",
        neo4j_password="custom_pass",
        debug=True,
        agent_memory_size=500,
        agent_timeout=60
    )

    assert settings.neo4j_uri == "bolt://custom:7687"
    assert settings.neo4j_user == "custom_user"
    assert settings.neo4j_password == "custom_pass"
    assert settings.debug == True
    assert settings.agent_memory_size == 500
    assert settings.agent_timeout == 60


def test_settings_copy():
    """Test settings copy functionality."""
    original = Settings(neo4j_uri="bolt://original:7687")

    # Create a copy with modifications
    copied = original.model_copy(update={"neo4j_uri": "bolt://copied:7687"})

    assert original.neo4j_uri == "bolt://original:7687"
    assert copied.neo4j_uri == "bolt://copied:7687"


def test_settings_serialization():
    """Test settings serialization."""
    settings = Settings()

    # Should be able to serialize to dict
    settings_dict = settings.model_dump()

    assert isinstance(settings_dict, dict)
    assert 'neo4j_uri' in settings_dict
    assert 'neo4j_user' in settings_dict
    assert 'neo4j_password' in settings_dict
    assert 'debug' in settings_dict


def test_settings_type_conversion():
    """Test settings type conversion from environment."""
    with patch.dict(os.environ, {
        'AGENT_MEMORY_SIZE': '5000',
        'AGENT_TIMEOUT': '120',
        'DEBUG': 'true',
        'CLI_COLOR_OUTPUT': 'false'
    }):
        settings = Settings()

        assert isinstance(settings.agent_memory_size, int)
        assert settings.agent_memory_size == 5000
        assert isinstance(settings.agent_timeout, int)
        assert settings.agent_timeout == 120
        assert isinstance(settings.debug, bool)
        assert settings.debug == True
        assert isinstance(settings.cli_color_output, bool)
        assert settings.cli_color_output == False


def test_database_url_with_different_protocols():
    """Test database URL construction with different protocols."""
    # Test with bolt protocol
    settings_bolt = Settings(neo4j_uri="bolt://example.com:7687")
    assert "bolt://" in settings_bolt.database_url

    # Test with neo4j protocol
    settings_neo4j = Settings(neo4j_uri="neo4j://example.com:7687")
    assert "neo4j://" in settings_neo4j.database_url


def test_settings_field_validation():
    """Test specific field validation."""
    settings = Settings()

    # Test that string fields are strings
    assert isinstance(settings.neo4j_uri, str)
    assert isinstance(settings.neo4j_user, str)
    assert isinstance(settings.app_name, str)

    # Test that int fields are integers
    assert isinstance(settings.agent_memory_size, int)
    assert isinstance(settings.agent_timeout, int)
    assert isinstance(settings.max_graph_size, int)

    # Test that bool fields are booleans
    assert isinstance(settings.debug, bool)
    assert isinstance(settings.cli_color_output, bool)


def test_get_settings_function():
    """Test get_settings function."""
    from src.config.settings import get_settings

    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.neo4j_uri is not None


def test_settings_env_file_config():
    """Test settings env file configuration."""
    settings = Settings()

    # Check that model config is properly set
    assert hasattr(settings, 'model_config')
    config = settings.model_config
    assert 'env_file' in config
    assert config['env_file'] == '.env'
    assert config['case_sensitive'] == False


def test_settings_field_descriptions():
    """Test that fields have proper descriptions."""
    settings = Settings()

    # Check that fields have descriptions in their Field definitions
    fields = settings.model_fields
    assert 'neo4j_uri' in fields
    assert 'neo4j_user' in fields
    assert 'neo4j_password' in fields

    # Check that Field objects have descriptions
    neo4j_uri_field = fields['neo4j_uri']
    assert hasattr(neo4j_uri_field, 'description')
    assert neo4j_uri_field.description is not None


def test_settings_extra_fields_ignored():
    """Test that extra fields are ignored according to model config."""
    # This should not raise an error due to extra="ignore" in model config
    settings = Settings(unknown_field="ignored")

    # The unknown field should not be present
    assert not hasattr(settings, 'unknown_field')


def test_database_url_edge_cases():
    """Test database URL construction edge cases."""
    # Test with URI without protocol
    settings_no_protocol = Settings(
        neo4j_uri="localhost:7687",
        neo4j_user="user",
        neo4j_password="pass"
    )
    url = settings_no_protocol.database_url
    assert "bolt://user:pass@localhost:7687" in url

    # Test with complex URI
    settings_complex = Settings(
        neo4j_uri="bolt+ssc://cluster.example.com:7687",
        neo4j_user="user",
        neo4j_password="pass"
    )
    url = settings_complex.database_url
    assert "bolt+ssc://user:pass@cluster.example.com:7687" in url
