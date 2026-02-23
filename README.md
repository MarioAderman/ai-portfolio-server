# Mario AI Portfolio

Dual-protocol AI portfolio server — an **MCP server** for structured tool access and an **A2A agent** ("Have You Met Mario?") for conversational discovery. Both serve the same data about my experience, skills, projects, and services.

## Why This Exists

Traditional portfolios are static. This one lets potential clients interact with my portfolio using their own AI tools — ask specific questions, get structured answers, and discover what I can do for them. The medium demonstrates the skill being sold.

## Architecture

```
mario-ai-portfolio/
├── src/
│   ├── mcp_server.py        # FastMCP server — 7 tools (port 8000)
│   ├── a2a_server.py        # A2A agent — (port 9000)
│   └── data/                # Shared content modules
│       ├── about.py
│       ├── skills.py
│       ├── services.py
│       ├── projects.py
│       ├── experience.py
│       └── contact.py
├── Dockerfile.mcp           # MCP server container
├── Dockerfile.a2a           # A2A agent container
└── pyproject.toml
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
claude mcp add mario-portfolio --transport http https://mcp.fintegra.solutions/mcp
```

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mario-portfolio": {
      "url": "https://mcp.fintegra.solutions/mcp"
    }
  }
}
```

**Cursor / VS Code** — add to `.cursor/mcp.json` or `.vscode/mcp.json`:

```json
{
  "servers": {
    "mario-portfolio": {
      "url": "https://mcp.fintegra.solutions/mcp"
    }
  }
}
```

Then just ask your AI assistant anything about Mario — skills, projects, services, availability.

## A2A Agent — "Have You Met Mario?"

Conversational agent-to-agent interface powered by Llama 3.1 8B via HF Inference API. Supports agent discovery via the [A2A protocol](https://google.github.io/A2A/).

- **Agent Card:** `https://agent.fintegra.solutions/.well-known/agent-card.json`
- **Skills:** portfolio_query, service_inquiry, availability_check

### Interact with the A2A Agent

**Discover the agent** — fetch the Agent Card:

```bash
curl https://agent.fintegra.solutions/.well-known/agent-card.json
```

**Send a message** — via JSON-RPC 2.0:

```bash
curl https://agent.fintegra.solutions/ \
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

async with A2AClient(url="https://agent.fintegra.solutions/") as client:
    card = await client.get_card()
    print(card.name)  # "Have You Met Mario? — AI Automation Engineer"

    response = await client.send_message(
        message={"role": "user", "parts": [{"kind": "text", "text": "What services do you offer?"}], "messageId": "msg-001"}
    )
    print(response)
```

Any A2A-compatible agent or orchestrator can discover and interact with this agent automatically via the Agent Card endpoint.

## Tech Stack

- **MCP:** [FastMCP](https://github.com/jlowin/fastmcp) v2 — Python, Streamable HTTP
- **A2A:** [a2a-sdk](https://github.com/a2aproject/a2a-python) — Official SDK, JSON-RPC 2.0
- **LLM:** Llama 3.1 8B Instruct via HF Inference API
- **Deployment:** Docker, EasyPanel, Hostinger VPS
- **Domain:** `fintegra.solutions` (subdomains: `mcp.*`, `agent.*`)

## Run Locally

```bash
# MCP server (port 8000)
uv run python -m src.mcp_server

# A2A agent (port 9000) — requires HF_TOKEN in .env
uv run python -m src.a2a_server
```

## Deployment

Two Docker services deployed via EasyPanel on Hostinger VPS:

| Service | Dockerfile | Port | Domain |
|---------|-----------|------|--------|
| MCP Server | `Dockerfile.mcp` | 8000 | `mcp.fintegra.solutions` |
| A2A Agent | `Dockerfile.a2a` | 9000 | `agent.fintegra.solutions` |

HTTPS via Let's Encrypt (managed by EasyPanel/Traefik).

## License

MIT
