"""Configuration management for the social graph AI agent system."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Neo4j Database Configuration
    neo4j_uri: str = Field(
        default="bolt://localhost:7687",
        description="Neo4j database connection URI"
    )
    neo4j_user: str = Field(
        default="neo4j",
        description="Neo4j database username"
    )
    neo4j_password: str = Field(
        default="password123",
        description="Neo4j database password"
    )
    neo4j_database: str = Field(
        default="neo4j",
        description="Neo4j database name"
    )

    # Application Configuration
    app_name: str = Field(
        default="Robo People's Person",
        description="Application name"
    )
    app_version: str = Field(
        default="0.1.0",
        description="Application version"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    # CLI Configuration
    cli_output_format: str = Field(
        default="table",
        description="Default CLI output format (table, json, csv)"
    )
    cli_color_output: bool = Field(
        default=True,
        description="Enable colored CLI output"
    )

    # Agent Configuration
    agent_memory_size: int = Field(
        default=1000,
        description="Maximum conversation memory size for agents"
    )
    agent_timeout: int = Field(
        default=30,
        description="Agent operation timeout in seconds"
    )

    # Network Analysis Configuration
    max_graph_size: int = Field(
        default=10000,
        description="Maximum nodes for in-memory graph analysis"
    )
    export_batch_size: int = Field(
        default=1000,
        description="Batch size for data export operations"
    )

    @property
    def database_url(self) -> str:
        """Construct the full database URL with credentials.

        Returns:
            str: Complete Neo4j connection URL with credentials.
        """
        # Extract the host part from the URI
        if "://" in self.neo4j_uri:
            protocol, host = self.neo4j_uri.split("://", 1)
        else:
            protocol, host = "bolt", self.neo4j_uri

        return f"{protocol}://{self.neo4j_user}:{self.neo4j_password}@{host}"


def get_settings() -> Settings:
    """Get application settings singleton.

    Returns:
        Settings: Application settings instance.
    """
    return Settings()


# Global settings instance
# settings = get_settings()
