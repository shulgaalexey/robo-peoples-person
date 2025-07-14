## FEATURE:
- AI Agent that maintains and processes social graphs and allows adding new people to storage and save relationships between people.
- Local-only usage on a single machine.
- Interactive Chat CLI for user interaction.
- Generates network insights (e.g., centrality metrics, community detection) and answers user queries.
- Creates analytical snapshots (exportable JSON/CSV reports) of the storage.
- Utilizes a graph database backend (e.g., Neo4j) behind the scenes.
- Builds upon the LangGraph library for graph processing.

## EXAMPLES:
- Add a person and a relationship:
  ```
  > add_person --name Alice --age 30
  Person 'Alice' added.
  > add_person --name Bob --age 25
  Person 'Bob' added.
  > add_relation --from Alice --to Bob --type friend
  Relationship 'friend' between 'Alice' and 'Bob' added.
  ```
- Query network insights:
  ```
  > insights --metric centrality
  Alice: 0.75
  Bob: 0.25
  ```
- Ask a question:
  ```
  > query "Who are Alice's friends?"
  Result: Bob
  ```

## DOCUMENTATION:
- LangGraph: https://github.com/langgraph/langgraph
- Graph database (e.g., Neo4j Python driver): https://neo4j.com/docs/api/python-driver/current/
- CLI framework (Click): https://click.palletsprojects.com/
- Pydantic: https://pydantic-docs.helpmanual.io/

## OTHER CONSIDERATIONS:
- CLI designed for PowerShell on Windows; use `.
venv\Scripts\Activate.ps1` to activate the virtual environment.
- Configuration through `.env` files and python-dotenv.
- Python 3.11+ required.
- Person data model to include attributes like name, age, location, etc.
- Snapshot exports should support JSON and CSV formats.
- Network insights requirements: centrality, community detection, path queries.
- All feature prompts and examples stored under `prompts/`.

## CONFIGURATION:
- Graph database: Neo4j (most popular with a Python driver).
- Network insights: support relationship path queries and directed expectation queries (e.g., relations between A and B, does C expect anything from D).
- Analytical snapshots: triggered manually via a CLI command.
- CLI commands: default set only (add_person, add_relation, insights, query) and natural English chat support.
- Relationship types: dynamic and user-defined per person; support both unidirectional and bidirectional relations.
