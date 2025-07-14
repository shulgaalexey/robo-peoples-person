### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use the virtual environment** whenever executing Python commands, including for unit tests. On Windows, activate with `.\.venv\Scripts\Activate.ps1` in PowerShell.
- **Store all prompts in `./prompts/` folder** - this is the central location for all prompts, PRPs, examples, and command templates. Exception: copilot-instructions.md stays in `./.github/` folder.

### 🖥️ Windows/PowerShell Environment
- **Environment**: Windows 11 with PowerShell 7
- **Editor**: VS Code with GitHub Copilot
- **Package Manager**: uv for fast dependency management
- **Command Chaining**: Use `;` instead of `&&` for multiple commands in PowerShell
- **Path Separators**: Use forward slashes `/` in Python code, backslashes `\` only in PowerShell paths
- **Virtual Environment**: Always use `.\.venv\Scripts\Activate.ps1` for activation

### 🤖 GitHub Copilot Integration
- **Leverage Copilot Chat**: For architectural discussions and complex problem solving
- **Use Agent Mode**: `#github-pull-request_copilot-coding-agent` for feature implementation
- **Inline Suggestions**: Accept for boilerplate code, review for business logic
- **Code Reviews**: Use Copilot to review and suggest improvements

### 📋 PRP (Project Request Proposal) Workflow
All PRPs and templates are stored in `./prompts/` folder:
1. **Generate PRP**: Use `prompts/commands/generate-prp.md` template
2. **Research**: Include comprehensive context and external references
3. **Plan**: Break down into tasks with clear validation gates
4. **Execute**: Use `prompts/commands/execute-prp.md` for implementation
5. **Validate**: Run all quality checks before completion
6. **Store**: Save all PRPs in `prompts/PRPs/` directory

### 🔧 Essential Commands (PowerShell)
```powershell
# Virtual Environment
.\.venv\Scripts\Activate.ps1                # Activate virtual environment
deactivate                                 # Deactivate virtual environment

# Development
uv sync                                     # Sync dependencies
uv add package-name                         # Add new dependency
uv remove package-name                      # Remove dependency

# Quality Checks
ruff check --fix; mypy .                    # Lint and type check
uv run pytest tests/ -v                     # Run tests
uv run pytest tests/ --cov=src --cov-report=term-missing  # Tests with coverage

# Application
uv run python -m src.main                   # Run main application (future)
```

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic
    - `tools.py` - Tool functions used by the agent
    - `prompts.py` - System prompts (store actual prompts in `./prompts/` folder)
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_dotenv()** for environment variables.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
- **Coverage**: Minimum 80% code coverage required
- **Types**: Include unit tests, integration tests, and end-to-end tests
- **Pattern**: Each feature needs happy path, edge case, and failure tests

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a "Discovered During Work" section.

### 🎨 Style & Conventions
- **Use Python** as the primary language (3.11+).
- **Follow PEP8**, use type hints, and format with `ruff` and `mypy`.
- **Use `pydantic` for data validation** and Pydantic AI for agent development.
- **Functions**: All new functions must have Google-style docstrings and type hints
- **Classes**: PascalCase naming, prefer composition over inheritance
- **Async**: Use async/await patterns for all agent operations
- **Type Safety**: Use Pydantic models for all data validation
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 🤖 AI Agent Development Guidelines
- **Async First**: All agent operations must be asynchronous
- **Tool Pattern**: Use tools for external interactions, avoid direct API calls in agents
- **Context Management**: Properly handle conversation context and state
- **Error Handling**: Implement graceful error handling and recovery
- **Validation**: Use Pydantic models for all inputs and outputs

### 🚫 Do Not Touch
- **Legacy Code**: Don't modify working implementations without explicit requirements
- **Generated Files**: Don't manually edit auto-generated configuration files
- **External Dependencies**: Don't modify external library code directly
- **Git History**: Don't rewrite commit history on shared branches

### 🔧 Environment Variables
- **Development**: Use `.env.local` file (gitignored)
- **Documentation**: Update `.env.example` when adding new variables
- **Loading**: Always use `python-dotenv` for environment variable loading
- **Validation**: Validate required environment variables on application startup

### ✅ Quality Gates
Before any commit or pull request:
```powershell
# Must pass all of these checks
ruff check --fix                            # Code formatting and linting
mypy .                                       # Type checking
uv run pytest tests/ -v --cov=src --cov-report=term-missing  # Testing with coverage
```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.
- **Keep inline documentation focused on 'why' not 'what'**

### 🔧 Troubleshooting
- **Virtual Environment Issues**: Ensure PowerShell execution policy allows script execution. Use `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` if needed
- **Package Management Issues**: Use `uv` for faster dependency resolution. Clear cache with `uv cache clean` if installation issues occur
- **Testing Issues**: Run tests with `-v` flag for verbose output. Use `--pdb` flag to drop into debugger on test failures

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.
- **Use structured exceptions with clear error messages for error handling**
- **Use structured logging with appropriate levels**
- **Use Pydantic Settings for configuration management**

### 🎯 Project Goals & Common Patterns
- Build production-ready AI agents for social interactions
- Demonstrate modern Python development practices on Windows
- Showcase effective GitHub Copilot integration patterns
- Create reusable patterns for future AI agent projects
- **Packaging**: Use modern Python packaging with `pyproject.toml`
- **Dependencies**: Pin exact versions for reproducible builds
- **Scripts**: All deployment scripts must be PowerShell compatible