"""Installation validation script for the Workplace Social Graph AI Agent."""

import os
import sys
from pathlib import Path


def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists and report the result."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False


def check_directory_structure():
    """Check that all required directories and files exist."""
    print("🔍 Checking project structure...")

    files_to_check = [
        # Core files
        ("pyproject.toml", "Project configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("README.md", "Documentation"),

        # Source code structure
        ("src/__init__.py", "Main package init"),
        ("src/main.py", "Main entry point"),

        # Configuration
        ("src/config/__init__.py", "Config package"),
        ("src/config/settings.py", "Settings module"),

        # Database layer
        ("src/database/__init__.py", "Database package"),
        ("src/database/models.py", "Data models"),
        ("src/database/neo4j_manager.py", "Neo4j manager"),
        ("src/database/migrations.py", "Database migrations"),

        # Analysis layer
        ("src/analysis/__init__.py", "Analysis package"),
        ("src/analysis/network_analysis.py", "Network analysis"),
        ("src/analysis/export_manager.py", "Export manager"),

        # Agents
        ("src/agents/__init__.py", "Agents package"),
        ("src/agents/social_graph_agent.py", "Main agent"),
        ("src/agents/insights_agent.py", "Insights agent"),
        ("src/agents/tools.py", "Agent tools"),

        # CLI
        ("src/cli/__init__.py", "CLI package"),
        ("src/cli/main.py", "CLI main"),

        # Tests
        ("tests/conftest.py", "Test configuration"),
        ("tests/test_config.py", "Config tests"),
        ("tests/test_models.py", "Model tests"),
        ("tests/test_agents.py", "Agent tests"),
        ("tests/test_cli.py", "CLI tests"),

        # Examples
        ("examples/demo.py", "Demo script"),
    ]

    all_good = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_good = False

    return all_good


def check_python_version():
    """Check Python version compatibility."""
    print("🐍 Checking Python version...")
    version = sys.version_info

    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"❌ Python version: {version.major}.{version.minor}.{version.micro} (requires Python 3.11+)")
        return False


def check_imports():
    """Check if core modules can be imported (basic syntax check)."""
    print("📦 Checking module imports...")

    modules_to_check = [
        "src.config.settings",
        "src.database.models",
        "src.agents.tools",
    ]

    all_imports_good = True

    for module_name in modules_to_check:
        try:
            # Try to compile the module without executing
            file_path = module_name.replace(".", "/") + ".py"
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                try:
                    compile(content, file_path, 'exec')
                    print(f"✅ {module_name}: Syntax OK")
                except SyntaxError as e:
                    print(f"❌ {module_name}: Syntax Error - {e}")
                    all_imports_good = False
            else:
                print(f"❌ {module_name}: File not found")
                all_imports_good = False

        except Exception as e:
            print(f"❌ {module_name}: Error - {e}")
            all_imports_good = False

    return all_imports_good


def print_next_steps():
    """Print next steps for the user."""
    print("\n🚀 Next Steps:")
    print("1. Install dependencies: pip install -e .")
    print("2. Start Neo4j database: docker-compose up -d")
    print("3. Initialize database: python -m src.main setup init-db")
    print("4. Run demo: python examples/demo.py")
    print("5. Try interactive CLI: python -m src.main chat")
    print("\n📚 Documentation:")
    print("• See README.md for comprehensive documentation")
    print("• Check examples/demo.py for usage examples")
    print("• Use 'python -m src.main --help' for CLI help")


def main():
    """Main validation function."""
    print("🤖 Workplace Social Graph AI Agent - Installation Validation")
    print("=" * 60)

    results = []

    # Check Python version
    results.append(check_python_version())
    print()

    # Check directory structure
    results.append(check_directory_structure())
    print()

    # Check basic imports
    results.append(check_imports())
    print()

    # Summary
    if all(results):
        print("🎉 SUCCESS: Installation validation passed!")
        print("All core components are properly installed and configured.")
    else:
        print("⚠️  WARNING: Some validation checks failed.")
        print("Please review the errors above and fix any issues.")

    print_next_steps()


if __name__ == "__main__":
    main()
