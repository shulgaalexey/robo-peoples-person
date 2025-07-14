#!/usr/bin/env python3
"""Minimal test for settings import."""

import sys

sys.path.insert(0, 'src')

print("About to import settings...")
from config.settings import Settings

print("Settings imported successfully!")

settings = Settings()
print("Settings instance created successfully!")
print(f"Neo4j URI: {settings.neo4j_uri}")
