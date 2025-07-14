#!/usr/bin/env python3
"""Debug script to test CLI functionality."""

import sys
import traceback

try:
    print("Testing basic imports...")
    import asyncio
    import json
    from pathlib import Path
    from typing import Optional

    import click
    print("✅ Basic imports successful")

    print("Testing pydantic imports...")
    from pydantic import Field
    from pydantic_settings import BaseSettings, SettingsConfigDict
    print("✅ Pydantic imports successful")

    print("Testing config module...")
    import src.config.settings
    print("✅ Config module imported")

    print("Getting Settings class...")
    Settings = src.config.settings.Settings
    print("✅ Settings class retrieved")

    print("Creating Settings instance...")
    settings = Settings()
    print("✅ Settings instance created successfully")

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Traceback: {traceback.format_exc()}")
