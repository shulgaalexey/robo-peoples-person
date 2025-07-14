# Copilot Instructions for Robo People's Person

## Project Overview
Robo People's Person is an AI Agent that analyzes and manages social interactions in workplace environments. It uses Neo4j for graph database storage and provides insights on network connectivity, collaboration patterns, and relationship recommendations.

## Development Guidelines

### Code Generation Best Practices
1. **Always follow async/await patterns** for database operations
2. **Use proper type hints** throughout the codebase
3. **Follow the existing project structure** in `src/` directory
4. **Use Pydantic models** for data validation and serialization
5. **Implement proper error handling** with try/catch blocks and logging

### Testing Standards
1. **Maintain 80%+ test coverage** (currently at 83.60%)
2. **Use AsyncMock for async methods** and Mock for synchronous methods
3. **Always mock external dependencies** (Neo4j, network analyzers, etc.)
4. **Write comprehensive test scenarios** covering success and error cases
5. **Use proper test fixtures** for consistent test setup

### Database Operations
1. **Use async context managers** for Neo4j sessions
2. **Implement proper connection handling** with connect/close patterns
3. **Follow Cypher query best practices** for Neo4j operations
4. **Use parameterized queries** to prevent injection attacks
5. **Handle database exceptions** gracefully

### Project File Structure
```
src/
├── agents/          # AI agents and tools
├── analysis/        # Network analysis and export functionality
├── cli/            # Command-line interface
├── config/         # Settings and configuration
└── database/       # Neo4j models and management
```

### Key Dependencies
- **Pydantic**: Data validation and settings management
- **Neo4j**: Graph database for relationship storage
- **NetworkX**: Graph analysis algorithms
- **AsyncIO**: Asynchronous programming support
- **Click**: CLI framework
- **Pytest**: Testing framework with async support

### Documentation Requirements
1. **Update PROGRESS.md** for any significant changes or completions
2. **Include docstrings** for all public methods and classes
3. **Add type hints** for function parameters and return values
4. **Comment complex logic** especially in graph algorithms
5. **Maintain clear commit messages** describing changes

### Performance Considerations
1. **Use async operations** for I/O bound tasks
2. **Batch database operations** when possible
3. **Implement proper caching** for frequently accessed data
4. **Monitor query performance** in Neo4j operations
5. **Use appropriate data structures** for graph processing

### Error Handling Patterns
1. **Log errors appropriately** using the logging module
2. **Return meaningful error messages** to users
3. **Handle connection failures** gracefully
4. **Validate input data** before processing
5. **Use custom exceptions** for domain-specific errors

### Testing Patterns
1. **Mock external dependencies** consistently
2. **Test both success and failure scenarios**
3. **Use proper async test decorators** (@pytest.mark.asyncio)
4. **Verify mock calls** in assertions
5. **Clean up test data** after test execution

## Special Instructions

### Progress Tracking
**IMPORTANT**: Always update PROGRESS.md when:
- Completing major features or fixes
- Reaching significant milestones
- Resolving test failures
- Implementing new functionality
- Making breaking changes

Include:
- ✅ Completed tasks with clear status
- 📊 Current metrics (test count, coverage percentage)
- 🎯 Summary of achievements
- 🔧 Any ongoing work or technical debt

### Neo4j Integration
When working with Neo4j:
1. Use the existing Neo4jManager class
2. Implement proper session management
3. Follow the established query patterns
4. Add new methods to the manager for reusability
5. Test database operations with mocked sessions

### Network Analysis
When implementing analysis features:
1. Use NetworkX for graph algorithms
2. Cache graph data when appropriate
3. Implement efficient traversal algorithms
4. Provide meaningful insights and visualizations
5. Handle edge cases like disconnected graphs

## Current Project Status
- **Test Coverage**: 83.60% (exceeds 80% target)
- **Total Tests**: 267 (all passing)
- **Last Updated**: July 14, 2025
- **Status**: All major functionality complete with comprehensive test coverage
