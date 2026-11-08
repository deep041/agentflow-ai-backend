# AgentFlow AI — Backend

Python/FastAPI backend for **AgentFlow AI**, a portfolio project exploring LLM integration, structured outputs, web research, custom function calling, and eventually multi-agent orchestration. The Angular frontend is maintained in a separate Git repository.

> **Project status:** Learning project through Phase 2.2. The capabilities below follow the implementation walkthrough; check your repository before marking them production-ready.

## Features

- **AI Planner:** Generates structured task plans using OpenAI and Pydantic.
- **Task persistence:** Saves generated plans and usage metadata to PostgreSQL.
- **Research Agent:** Uses OpenAI hosted web search to produce a report and source references.
- **Custom Tool Agent:** Requests and executes allowlisted Python tools through an OpenAI function-calling loop.
- **Execution trace:** Returns tool names, arguments, outputs, and iteration count.
- **Usage metadata:** Captures model, input/output tokens, and request latency for planner requests.

### Available custom tools

| Tool | Description |
| --- | --- |
| `calculate` | Safely evaluates basic arithmetic using Python AST |
| `get_current_datetime` | Returns the current UTC date/time |
| `search_knowledge_base` | Performs keyword search against local example documents |

The knowledge-base tool is **keyword retrieval, not vector RAG**. The current agent is a bounded function-calling loop, **not yet a LangGraph multi-agent system**.

## Tech stack

- Python 3.12+ (subject to package compatibility)
- FastAPI, Uvicorn, Pydantic / pydantic-settings
- OpenAI Python SDK / Responses API
- PostgreSQL, SQLAlchemy async, asyncpg, Alembic
- pytest, pytest-asyncio, httpx

## Getting started

### Prerequisites

- Python and pip
- PostgreSQL server
- OpenAI API key with appropriate model/tool access and billing

### Setup

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies (use the project's pinned `requirements.txt` when available):

```bash
pip install fastapi "uvicorn[standard]" openai pydantic-settings python-dotenv "sqlalchemy[asyncio]" asyncpg alembic pytest pytest-asyncio httpx
```

Create a PostgreSQL database named `agentflow` and create `.env`:

```dotenv
OPENAI_API_KEY=replace_with_your_key
OPENAI_MODEL=gpt-4.1-mini
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/agentflow
```

Model availability and hosted web-search support vary. Choose a model supported by your account and the API features you use.

**Never commit `.env`, API keys, or database passwords.** Provide a sanitized `.env.example` in the repository.

### Database migrations

If Alembic has already been configured for the project's async SQLAlchemy metadata:

```bash
alembic upgrade head
```

For a fresh Alembic setup, configure `migrations/env.py` with the application database URL and `Base.metadata` before generating migrations. Review generated migrations before applying them.

### Run the API

From the backend repository root:

```bash
uvicorn app.main:app --reload
```

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## API reference

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/planner/generate` | Generate a structured plan |
| `POST` | `/api/v1/tasks` | Generate and save a plan |
| `GET` | `/api/v1/tasks` | List recent plans |
| `GET` | `/api/v1/tasks/{id}` | Retrieve a saved plan |
| `POST` | `/api/v1/research` | Generate a web-assisted research report |
| `POST` | `/api/v1/agent/run` | Execute the custom tool agent |

### Example: create a plan

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"goal":"Research AI coding assistants and prepare a comparison report"}'
```

### Example: run the tool agent

```bash
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"message":"Calculate (150 * 3) / 30 and give the current UTC date"}'
```

## Suggested source layout

```text
app/
├── agents/
│   ├── researcher.py
│   └── tool_agent.py
├── api/routes/
│   ├── planner.py
│   ├── tasks.py
│   ├── research.py
│   └── agent.py
├── core/
│   ├── config.py
│   └── database.py
├── models/task.py
├── schemas/
├── services/planner_service.py
├── tools/
│   ├── calculator.py
│   ├── datetime_tool.py
│   ├── knowledge.py
│   └── registry.py
└── main.py
tests/
migrations/
```

## Testing

```bash
python -m pytest -q
```

Use mocked OpenAI responses for repeatable tests without API charges. Add integration tests for migrations, API validation, tool dispatch, malformed arguments, execution limits, and error responses.

## Architecture

```text
Angular client (separate repo)
         |
      REST API
         |
       FastAPI
         |
  +------+-------+
  |              |
Planner       Research / Tool Agent
  |              |
OpenAI        OpenAI Responses API
  |              |
PostgreSQL    Hosted web search / allowlisted Python tools
```

## Safety and production limitations

This implementation is a **development prototype**, not a production-hardened service. Before public deployment:

- Add authentication, per-user authorization, rate limits, and usage budgets.
- Independently validate tool arguments and enforce per-tool permissions.
- Bound tool calls, iterations, execution time, output size, and total cost.
- Avoid exposing internal exception messages or sensitive tool results.
- Defend against prompt injection in retrieved content.
- Add structured logs, request IDs, and durable run persistence.
- Verify citations and model-generated claims; structured JSON does not guarantee factual accuracy.

## Roadmap

- [x] Phase 1: Structured AI task planner (implementation walkthrough)
- [x] Phase 1.5: PostgreSQL task storage and usage metadata (implementation walkthrough)
- [x] Phase 2.1: Hosted web research (implementation walkthrough)
- [x] Phase 2.2: Custom tools and bounded agent loop (implementation walkthrough)
- [ ] Stronger tool argument validation and full agent-run persistence
- [ ] SSE streaming and background workers
- [ ] LangGraph orchestration of Planner, Researcher, Analyst, Writer, Reviewer
- [ ] Document ingestion, embeddings, and pgvector RAG
- [ ] Human-in-the-loop approvals, evaluations, observability, and deployment

> Checkboxes above are based on the tutorial progress, not a review of the actual Git repository.

## Related repository

**AgentFlow AI Frontend:** Add the frontend GitHub repository URL here.

## License

Add a license file if you intend to open-source this project.
