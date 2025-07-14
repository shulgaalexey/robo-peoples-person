"""Tests for the configuration module."""

import pytest
from pydantic import ValidationError

from src.config.settings import Settings


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()

    assert settings.neo4j_uri == "bolt://localhost:7687"
    assert settings.neo4j_username == "neo4j"
    assert settings.neo4j_database == "neo4j"
    assert settings.debug is False
    assert settings.log_level == "INFO"


def test_settings_from_env(monkeypatch):
    """Test settings loaded from environment variables."""
    monkeypatch.setenv("NEO4J_URI", "bolt://test:7687")
    monkeypatch.setenv("NEO4J_USERNAME", "testuser")
    monkeypatch.setenv("NEO4J_PASSWORD", "testpass")
    monkeypatch.setenv("DEBUG", "true")

    settings = Settings()

    assert settings.neo4j_uri == "bolt://test:7687"
    assert settings.neo4j_username == "testuser"
    assert settings.neo4j_password == "testpass"
    assert settings.debug is True


def test_settings_validation():
    """Test settings validation."""
    # Valid settings
    settings = Settings(
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j",
        neo4j_password="password"
    )
    assert settings.neo4j_uri == "bolt://localhost:7687"

    # Invalid URI format should still work (validation could be added later)
    settings = Settings(neo4j_uri="invalid-uri")
    assert settings.neo4j_uri == "invalid-uri"


def test_database_url_property():
    """Test the database_url property."""
    settings = Settings(
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="testuser",
        neo4j_password="testpass"
    )

    expected_url = "bolt://testuser:testpass@localhost:7687"
    assert settings.database_url == expected_url


def test_database_url_without_credentials():
    """Test database_url when no password is provided."""
    settings = Settings(
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j"
    )

    # Should still include username even without password
    expected_url = "bolt://neo4j:@localhost:7687"
    assert settings.database_url == expected_url
