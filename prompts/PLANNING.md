# Robo People's Person - Project Planning

## Project Overview
AI Agent system designed to care about social interactions, built using modern Python development practices with GitHub Copilot integration and Windows/PowerShell compatibility.

## Architecture & Tech Stack

### Core Technologies
- **Language**: Python 3.11+
- **Framework**: Pydantic AI for agent development
- **Environment**: Windows with PowerShell
- **Development**: VS Code with GitHub Copilot
- **Dependencies**: uv for package management
- **Testing**: pytest with coverage
- **Linting**: ruff + mypy
- **Documentation**: Markdown

### Virtual Environment
- **Setup**: Use `python -m venv venv` in PowerShell
- **Activation**: `.\venv\Scripts\Activate.ps1` in PowerShell
- **Package Management**: `uv` for fast dependency resolution

## Project Structure & Conventions

### File Organization
```
robo-peoples-person/
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot configuration
├── prompts/
│   ├── commands/                  # Command templates for PRP generation/execution
│   ├── examples/                  # Example PRPs and patterns
│   └── PRPs/                      # Project Request Proposals
├── agents/                        # Core AI agent implementations
├── tools/                         # Agent tools and utilities
├── config/                        # Configuration management
├── tests/                         # Test files mirroring main structure
├── docs/                          # Additional documentation
├── PLANNING.md                    # This file - project planning and architecture
├── TASK.md                        # Task tracking and completion status
├── CLAUDE.md                      # Claude Code configuration
├── README.md                      # Project overview and setup
└── requirements.txt               # Python dependencies
```

### Naming Conventions
- **Files**: snake_case for Python files, kebab-case for documentation
- **Classes**: PascalCase
- **Functions/Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Modules**: Short, descriptive, lowercase names

### Code Organization Principles
- **Maximum file length**: 500 lines
- **Module separation**: Group by feature/responsibility
- **Agent structure**:  
  - `agent.py` - Main agent definition and execution
  - `tools.py` - Tool functions used by the agent
  - `prompts.py` - System prompts
- **Clear imports**: Prefer relative imports within packages
- **Type hints**: Required for all function signatures

## Development Workflow

### GitHub Copilot Integration
- Leverage GitHub Copilot Chat for architecture discussions
- Use inline suggestions for boilerplate code
- Utilize Copilot agent mode (`#github-pull-request_copilot-coding-agent`) for feature implementation
- Follow PRP (Project Request Proposal) pattern for complex features

### PRP (Project Request Proposal) System
1. **PRP Generation**: Use `prompts/commands/generate-prp.md` to create comprehensive feature specifications
2. **PRP Execution**: Use `prompts/commands/execute-prp.md` to implement features
3. **PRP Storage**: All PRPs stored in `prompts/PRPs/` directory
4. **Template**: Use `prompts/PRPs/templates/prp_base.md` as foundation

### Command Reference (PowerShell)
```powershell
# Virtual Environment
.\venv\Scripts\Activate.ps1

# Development
uv run python -m pytest tests/ -v          # Run tests
ruff check --fix; mypy .                   # Lint and type check
uv run python -m src.main                  # Run main application

# Package Management
uv add package-name                        # Add dependency
uv remove package-name                     # Remove dependency
uv sync                                    # Sync dependencies
```

## Quality Standards

### Testing Requirements
- **Coverage**: Minimum 80% test coverage
- **Test Structure**: Mirror main application structure in `/tests`
- **Test Types**: Unit tests, integration tests, end-to-end tests
- **Test Categories**:  
  - Happy path test
  - Edge case test
  - Failure case test

### Code Quality
- **Formatting**: Use `black` for code formatting
- **Linting**: `ruff` for style and error checking
- **Type Checking**: `mypy` for static type analysis
- **Documentation**: Google-style docstrings for all functions

### Validation Gates
All code must pass these checks before merge:
```powershell
# Syntax & Style
ruff check --fix
mypy .

# Tests
uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Integration (if applicable)
# Manual testing of main workflows
```

## AI Agent Architecture

### Core Principles
- **Modularity**: Each agent has specific, well-defined responsibilities
- **Tool-based**: Agents use tools for external interactions
- **Async-first**: All agent operations are asynchronous
- **Type-safe**: Pydantic models for all data structures
- **Context-aware**: Agents maintain conversation context

### Multi-Agent Patterns
- **Primary-Sub Agent**: Primary agent delegates to specialized sub-agents
- **Tool Integration**: Sub-agents can be used as tools by primary agents
- **Dependency Injection**: Use RunContext for passing dependencies
- **Token Tracking**: Pass usage context between agents

## Environment & Configuration

### Environment Variables
Use `python-dotenv` with `.env` files:
- **Development**: `.env.local` (gitignored)
- **Production**: `.env` (documented in `.env.example`)
- **Loading**: Use `load_dotenv()` in configuration modules

### Configuration Management
- **Settings**: Use `pydantic-settings` for configuration
- **Validation**: Validate all environment variables on startup
- **Defaults**: Provide sensible defaults for development

## Documentation Standards

### README Structure
- Project overview and purpose
- Installation and setup instructions
- Usage examples
- API documentation (if applicable)
- Contributing guidelines
- License information

### Code Documentation
- **Docstrings**: Google-style for all public functions
- **Comments**: Explain 'why' not 'what'
- **Inline comments**: Use `# Reason:` for complex logic
- **Type hints**: Required for all function parameters and returns

## Deployment & Distribution

### Packaging
- Use modern Python packaging standards
- Include all necessary metadata in `pyproject.toml`
- Pin dependencies for reproducible builds

### CI/CD Integration
- GitHub Actions for automated testing
- PowerShell-compatible scripts
- Windows-first deployment strategies

## Security Considerations

### Environment Security
- Never commit secrets to git
- Use `.env` files for local development
- Implement proper secret management for production

### AI Agent Security
- Validate all inputs to agents
- Implement rate limiting for external API calls
- Use structured outputs to prevent injection attacks

## Project Goals & Constraints

### Primary Goals
- Build production-ready AI agents
- Demonstrate modern Python development practices
- Showcase GitHub Copilot integration patterns
- Maintain Windows/PowerShell compatibility

### Constraints
- Windows development environment required
- PowerShell as primary shell
- GitHub Copilot as primary AI assistant
- Type safety throughout codebase
- Comprehensive testing required

## Evolution & Maintenance

### Version Management
- Semantic versioning for releases
- Keep CHANGELOG.md updated
- Tag releases in git

### Technical Debt Management
- Regular refactoring cycles
- Monitor file size limits (500 lines max)
- Update dependencies regularly
- Review and update documentation quarterly

## References & Resources

### Official Documentation
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [PowerShell Documentation](https://docs.microsoft.com/powershell)

### Best Practices
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Python Best Practices](https://realpython.com/python-application-layouts/)
- [Type Hint Best Practices](https://typing.readthedocs.io/en/latest/guides/writing_good_generics.html)
