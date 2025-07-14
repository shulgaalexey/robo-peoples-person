# Robo People's Person

> AI Agent that cares about social interactions

A modern Python project for building AI agents focused on social interaction capabilities, developed with Windows/PowerShell compatibility and GitHub Copilot integration.

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11** with PowerShell 7+
- **Python 3.11+**
- **VS Code** with GitHub Copilot extension
- **Git** for version control

### Installation

1. **Clone the repository**
   ```powershell
   git clone https://github.com/shulgaalexey/robo-peoples-person.git
   cd robo-peoples-person
   ```

2. **Set up virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies** (when available)
   ```powershell
   pip install uv  # Install uv first
   uv sync         # Install project dependencies
   ```

4. **Install development tools**
   ```powershell
   uv add --dev ruff mypy pytest pytest-cov black
   ```

## 📁 Project Structure

```
robo-peoples-person/
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot configuration
├── prompts/
│   ├── commands/                  # PRP generation and execution templates
│   ├── examples/                  # Example patterns and workflows
│   └── PRPs/                      # Project Request Proposals
├── agents/                        # AI agent implementations (future)
├── tools/                         # Agent tools and utilities (future)
├── tests/                         # Test files (future)
├── PLANNING.md                    # Project architecture and guidelines
├── TASK.md                        # Task tracking and management
├── CLAUDE.md                      # Claude Code configuration
└── README.md                      # This file
```

## 🎯 Development Workflow

This project uses a **PRP (Project Request Proposal)** system for feature development:

### 1. Planning Phase
- Check `TASK.md` for current priorities
- Review `PLANNING.md` for architecture guidelines
- Use GitHub Copilot Chat for design discussions

### 2. Feature Development
```powershell
# Generate a new PRP for your feature
# Use the template in prompts/commands/generate-prp.md

# Execute the PRP using GitHub Copilot
# Follow prompts/commands/execute-prp.md
```

### 3. Quality Assurance
```powershell
# Code formatting and linting
ruff check --fix; mypy .

# Run tests with coverage
uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Manual testing (when applicable)
uv run python -m src.main
```

## 🔧 Development Commands

### Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1        # Activate environment
deactivate                         # Deactivate environment
```

### Package Management
```powershell
uv add package-name                # Add dependency
uv remove package-name             # Remove dependency
uv sync                            # Sync all dependencies
```

### Code Quality
```powershell
ruff check --fix                   # Format and lint code
mypy .                             # Type checking
black .                            # Code formatting (alternative)
```

### Testing
```powershell
uv run pytest tests/               # Run all tests
uv run pytest tests/ -v            # Verbose test output
uv run pytest tests/ --cov=src     # Run with coverage
```

## 🤖 AI Agent Architecture

This project is designed to build AI agents using modern Python patterns:

- **Framework**: Pydantic AI for type-safe agent development
- **Async-First**: All agent operations use async/await patterns
- **Tool-Based**: Agents use tools for external interactions
- **Multi-Agent**: Support for agent-to-agent communication
- **Context-Aware**: Maintains conversation context and state

## 📋 Task Management

Tasks are managed using a priority-based system in `TASK.md`:

- **P-0**: Immediate tasks (urgent)
- **P-1**: Important tasks (next in line)
- **P-2**: Obligations (no urgency)
- **P-X**: Exciting tasks (motivation boosters)

## 🎨 Code Style

- **Type Hints**: Required for all function signatures
- **Docstrings**: Google-style for all public functions
- **Max Line Length**: 88 characters (Black default)
- **Max File Length**: 500 lines (refactor if longer)
- **Import Style**: Absolute imports, relative within packages

## 🧪 Testing Strategy

- **Coverage**: Minimum 80% required
- **Structure**: Tests mirror main application structure
- **Types**: Unit, integration, and end-to-end tests
- **Pattern**: Happy path, edge cases, and failure scenarios

## 🔄 GitHub Copilot Integration

This project is optimized for GitHub Copilot development:

- **Copilot Chat**: Used for architectural discussions
- **Agent Mode**: `#github-pull-request_copilot-coding-agent` for features
- **Inline Suggestions**: Leveraged for boilerplate code
- **PRP System**: Structured approach for complex features

## 📚 Documentation

- **PLANNING.md**: Complete project architecture and conventions
- **TASK.md**: Current tasks and priorities
- **CLAUDE.md**: Claude Code configuration for AI assistance
- **PRPs/**: Feature specifications and implementation guides

## 🛠️ Troubleshooting

### PowerShell Execution Policy
If you encounter script execution issues:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Virtual Environment Issues
Ensure you're using the correct activation script:
```powershell
# Correct (PowerShell)
.\venv\Scripts\Activate.ps1

# Incorrect (Command Prompt style)
venv\Scripts\activate.bat
```

### Package Installation Issues
Clear UV cache if you encounter installation problems:
```powershell
uv cache clean
uv sync
```

## 🤝 Contributing

1. Check `TASK.md` for current priorities
2. Review `PLANNING.md` for architecture guidelines
3. Create a PRP for new features using the templates
4. Use GitHub Copilot for implementation assistance
5. Ensure all quality gates pass before submitting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [PowerShell Documentation](https://docs.microsoft.com/powershell)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
