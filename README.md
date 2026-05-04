# Mario AI Portfolio

Dual-protocol AI portfolio server — an **MCP server** for structured tool access and an **A2A agent** ("Have You Met Mario?") for conversational discovery. Both serve the same data about my experience, skills, projects, and services.

## Why This Exists

Traditional portfolios are static. This one lets potential clients interact with my portfolio using their own AI tools — ask specific questions, get structured answers, and discover what I can do for them. The medium demonstrates the skill being sold.

## Architecture

```
mario-ai-portfolio/
├── src/
│   ├── server.py            # Combined ASGI dispatcher (production entry point)
│   ├── mcp_server.py        # FastMCP server — 7 tools
│   ├── a2a_server.py        # A2A agent — conversational interface
│   └── data/                # Shared content modules
│       ├── about.py
│       ├── skills.py
│       ├── services.py
│       ├── projects.py
│       ├── experience.py
│       └── contact.py
├── Dockerfile               # Combined production image
├── Dockerfile.mcp           # Standalone MCP server
├── Dockerfile.a2a           # Standalone A2A agent
└── render.yaml              # Render deployment config
```

## MCP Server

7 tools exposed via Streamable HTTP:

| Tool | Description |
|------|-------------|
| `get_about_me()` | Professional bio, background, timezone, availability |
| `get_skills(category?)` | Technical skills by category (ai, automation, backend, frontend) |
| `get_services()` | Service offerings and pricing approach |
| `get_projects()` | Summary list of portfolio projects |
| `get_project_detail(name)` | Deep-dive on a specific project |
| `get_experience()` | Professional timeline and education |
| `get_contact_info()` | Contact details and how to hire |

### Connect to the MCP Server

Add the following config to your MCP client of choice:

**Claude Code** — run in your terminal:

```bash
claude mcp add mario-portfolio --transport http https://<your-service>.onrender.com/mcp
```

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mario-portfolio": {
      "url": "https://<your-service>.onrender.com/mcp"
    }
  }
}
```

**Cursor / VS Code** — add to `.cursor/mcp.json` or `.vscode/mcp.json`:

```json
{
  "servers": {
    "mario-portfolio": {
      "url": "https://<your-service>.onrender.com/mcp"
    }
  }
}
```

Then just ask your AI assistant anything about Mario — skills, projects, services, availability.

## A2A Agent — "Have You Met Mario?"

Conversational agent-to-agent interface powered by Llama 3.1 8B via Groq. Supports agent discovery via the [A2A protocol](https://google.github.io/A2A/).

- **Agent Card:** `https://<your-service>.onrender.com/.well-known/agent.json`
- **Skills:** portfolio_query, service_inquiry, availability_check

### Interact with the A2A Agent

**Discover the agent** — fetch the Agent Card:

```bash
curl https://<your-service>.onrender.com/.well-known/agent.json
```

**Send a message** — via JSON-RPC 2.0:

```bash
curl https://<your-service>.onrender.com/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "What projects has Mario built?"}],
        "messageId": "msg-001"
      }
    }
  }'
```

**From Python** — using the a2a-sdk client:

```python
from a2a.client import A2AClient

async with A2AClient(url="https://<your-service>.onrender.com/") as client:
    card = await client.get_card()
    print(card.name)  # "Have You Met Mario? — AI Automation Engineer"
```

Any A2A-compatible agent or orchestrator can discover and interact with this agent automatically via the Agent Card endpoint.

## Tech Stack

- **MCP:** [FastMCP](https://github.com/jlowin/fastmcp) v3 — Python, Streamable HTTP
- **A2A:** [a2a-sdk](https://github.com/a2aproject/a2a-python) — Official SDK, JSON-RPC 2.0
- **LLM:** Llama 3.1 8B Instant via [Groq](https://groq.com)
- **Deployment:** Docker, [Render](https://render.com) (free tier)

## Run Locally

Requires `GROQ_API_KEY` in a `.env` file.

```bash
# Combined server (MCP + A2A on port 8000)
uv run python -m uvicorn src.server:app --reload

# Or run services independently:
uv run python -m uvicorn src.mcp_server:app --port 8000   # MCP only
uv run python -m uvicorn src.a2a_server:app --port 9000   # A2A only
```

Verify locally:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/.well-known/agent.json
```

## Deployment

Single Docker service deployed on [Render](https://render.com) free tier.

| Endpoint | Path |
|----------|------|
| Health | `/health` |
| MCP Server | `/mcp` |
| A2A Agent Card | `/.well-known/agent.json` |
| A2A Messages | `POST /` |

The service stays permanently warm via a [UptimeRobot](https://uptimerobot.com) monitor pinging `/health` every 5 minutes (free plan).

### Deploy your own

1. Fork this repo
2. Create a [Render](https://render.com) account (no credit card required)
3. **New → Web Service** → connect your fork — Render detects `render.yaml` automatically
4. Set environment variables:
   - `GROQ_API_KEY` — your [Groq API key](https://console.groq.com)
   - `AGENT_URL` — the Render service URL (set after first deploy)
5. Set up a free [UptimeRobot](https://uptimerobot.com) HTTP monitor on `/health` at 5-minute intervals

## License

MIT
