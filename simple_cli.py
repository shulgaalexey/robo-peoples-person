"""Simplified CLI test."""

import click


@click.group()
def cli():
    """Test CLI."""
    pass

@cli.command()
def test():
    """Test command."""
    click.echo("Test successful!")

if __name__ == '__main__':
    cli()
