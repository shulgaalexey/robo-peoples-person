#!/usr/bin/env python3
"""Test script to debug CLI issues."""

import os
import sys

# Add the project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Starting CLI test...")

try:
    from cli.main import cli
    print("CLI imported successfully")

    # Test help first
    print("Testing help...")
    sys.argv = ['test_cli.py', '--help']
    cli()
    print("Help completed")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
