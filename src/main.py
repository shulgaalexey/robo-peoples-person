"""Main entry point for the workplace social graph AI agent."""

import asyncio
import logging
import sys
from pathlib import Path

from .cli.main import cli
from .config.settings import Settings


def setup_logging(settings: Settings):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('workplace_social_graph.log')
        ]
    )


def main():
    """Main entry point."""
    # Setup basic logging
    settings = Settings()
    setup_logging(settings)

    # Run the CLI
    cli()


if __name__ == '__main__':
    main()
