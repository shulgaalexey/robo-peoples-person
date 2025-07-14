# Workplace Social Graph AI Agent

A comprehensive AI-powered system for managing and analyzing workplace social networks using graph database technology. This system helps organizations understand collaboration patterns, identify experts, and optimize team connectivity.

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
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install uv package manager**
   ```powershell
   pip install uv
   ```

4. **Install project dependencies**
   ```powershell
   uv sync
   ```

5. **Verify installation**
   ```powershell
   # Check that all commands are available
   wsg --help
   ```

   ### Command Line Interface

   The Workplace Social Graph (WSG) CLI provides comprehensive tools for managing workplace relationships:

   ```powershell
   # General help
   wsg --help

   # Person management
   wsg person add --name "John Doe" --email "john@company.com"
   wsg person list
   wsg person find-experts --skill "Python"
   wsg person who-to-ask --topic "AI development"

   # Organization analysis
   wsg org chart
   wsg org chart --department "Engineering"

   # Network insights
   wsg network insights
   wsg network collaboration --days 30
   wsg network silos
   wsg network daily-report
   wsg network recommend-connections --email "user@company.com"

   # Data management
   wsg data export --format csv --output ./export
   wsg data stats
   wsg data clear  # Use with caution!

   # Interactive chat mode
   wsg chat
   ```


## 🤖 AI Agent Scenarios

### SocialGraphAgent - Main Network Management Agent

The **SocialGraphAgent** is your primary interface for managing workplace relationships and finding people. Here are the top 5 scenarios where it excels:

#### 1. **New Employee Onboarding** 🆕
```bash
# Add new team member with complete profile
wsg person add --name "Sarah Wilson" --email "sarah@company.com" \
    --department "Engineering" --role "Junior Developer" \
    --skills "JavaScript" --skills "React" --location "Remote"

# Find potential mentors in the same field
wsg person find-experts --skill "JavaScript" --department "Engineering"

# Get networking recommendations for the new hire
wsg network insights --person "Sarah Wilson"
```
**Use Case**: HR teams can quickly integrate new employees into the social network and identify the best mentors and collaborators.

#### 2. **Expert Discovery for Projects** 🔍
```bash
# Find machine learning experts across the company
wsg person find-experts --skill "machine learning" --limit 10

# Get specific recommendations for AI project staffing
wsg person who-to-ask --topic "deep learning model deployment" \
    --expertise "MLOps"

# Check availability and connections of potential team members
wsg network insights --person "Dr. Jane Smith"
```
**Use Case**: Project managers can quickly identify the right experts for cross-functional teams and understand their network connections.

#### 3. **Organizational Structure Analysis** 🏢
```bash
# View complete organizational hierarchy
wsg org chart

# Analyze specific department structure
wsg org chart --department "Product Management"

# Export org data for leadership presentations
wsg data export --format csv --output ./quarterly_org_review
```
**Use Case**: Leadership teams can visualize reporting structures, identify management gaps, and plan organizational changes.

#### 4. **Knowledge Transfer Planning** 📚
```bash
# Find who to ask about legacy systems
wsg person who-to-ask --topic "legacy payment system architecture"

# Identify critical knowledge holders
wsg person find-experts --skill "COBOL" --skill "mainframe"

# Analyze knowledge concentration risks
wsg network insights --department "Infrastructure"
```
**Use Case**: IT teams can identify knowledge silos and plan knowledge transfer before key personnel leave or retire.

#### 5. **Cross-Team Collaboration Setup** 🤝
```bash
# Interactive mode for complex collaboration questions
wsg chat
# User: "I need to set up a cross-functional team for our mobile app rewrite.
#        Who should be involved from different departments?"

# Find the right mix of skills across departments
wsg person find-experts --skill "mobile development"
wsg person find-experts --skill "UI/UX design" --department "Design"
wsg person find-experts --skill "product strategy" --department "Product"
```
**Use Case**: Product owners can use natural language to get AI-powered recommendations for team composition and collaboration strategies.

### InsightsAgent - Advanced Analytics and Organizational Health

The **InsightsAgent** provides deep analytical insights into organizational dynamics and network health. Here are the top 5 scenarios for strategic decision-making:

#### 1. **Organizational Health Monitoring** 💚
```bash
# Generate comprehensive daily health report
wsg network daily-report

# Analyze collaboration patterns over the quarter
wsg network collaboration --days 90

# Check overall network statistics
wsg data stats
```
**Use Case**: Executive teams get daily insights into organizational connectivity, collaboration trends, and early warning signs of communication breakdowns.

#### 2. **Silo Detection and Prevention** 🚨
```bash
# Identify isolated departments and teams
wsg network silos

# Analyze department-specific connectivity issues
wsg network insights --department "Research & Development"

# Get actionable recommendations for improving cross-team collaboration
wsg network daily-report  # Includes specific recommendations
```
**Use Case**: Organizational development teams can proactively identify and address departmental silos before they impact productivity and innovation.

#### 3. **Strategic Workforce Planning** 📊
```bash
# Analyze collaboration patterns to identify high-value connectors
wsg network insights  # Shows most influential people and bridge connectors

# Get connection recommendations for key employees
wsg network recommend-connections --email "cto@company.com" --limit 10

# Export comprehensive network data for strategic analysis
wsg data export --format json --output ./strategic_analysis --include-sensitive
```
**Use Case**: C-suite executives can identify key influencers, plan succession strategies, and understand the informal power structures within the organization.

#### 4. **Team Restructuring and Mergers** 🔄
```bash
# Analyze impact before team restructuring
wsg network insights --department "Engineering"
wsg network insights --department "Product"

# Identify potential collaboration points between merging teams
wsg network collaboration --days 60

# Generate recommendations for maintaining connectivity during changes
wsg network recommend-connections --email "team-lead@company.com"
```
**Use Case**: During reorganizations or mergers, leadership can understand existing relationships and plan changes that preserve valuable connections.

#### 5. **Performance and Innovation Correlation** 🚀
```bash
# Analyze collaboration patterns of high-performing teams
wsg network insights --department "Innovation Lab"

# Identify collaboration trends that correlate with project success
wsg network collaboration --days 180

# Find patterns among most influential employees
wsg network insights  # Focus on top influencers section
```
**Use Case**: Performance management teams can identify collaboration patterns that drive innovation and replicate them across the organization.

## 💡 Agent Combination Strategies

**Power User Tip**: Combine both agents for maximum insight:

```bash
# Daily executive briefing workflow
wsg network daily-report                    # InsightsAgent: Overall health
wsg data stats                             # SocialGraphAgent: Quick metrics
wsg network silos                          # InsightsAgent: Risk assessment
wsg person find-experts --skill "leadership" # SocialGraphAgent: Key people
```

**Cross-Functional Project Setup**:
```bash
# 1. Find the right people (SocialGraphAgent)
wsg person find-experts --skill "data science"
wsg person who-to-ask --topic "customer analytics"

# 2. Analyze team dynamics (InsightsAgent)
wsg network insights --department "Data Science"
wsg network recommend-connections --email "project-lead@company.com"

# 3. Monitor collaboration (InsightsAgent)
wsg network collaboration --days 30  # Track project progress
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
.\.venv\Scripts\Activate.ps1        # Activate environment
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
.\.venv\Scripts\Activate.ps1

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
