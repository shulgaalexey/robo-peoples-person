#!/usr/bin/env python3
"""Simple test to check if CLI works."""

import click


@click.command()
@click.option('--name', default='World', help='Name to greet.')
def hello(name):
    """Simple program that greets NAME."""
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
