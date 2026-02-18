# CLAUDE.md — Mario AI Portfolio

## What This Is
A dual-protocol personal portfolio: MCP server + A2A agent. Both serve the same data about Mario's experience, skills, projects, and services. MCP exposes structured tools for LLMs. A2A provides a conversational agent for agent-to-agent delegation.

## Rules
- **Python:** Always run with `uv run python`, never `python` or `python3`
- **Secrets:** Never hardcode API keys or tokens. Use env vars from `.env`
- **Language:** All content in English (Upwork audience)
- **Content:** Shared data lives in `src/data/*.py` as plain Python dicts
- **MCP server:** `src/mcp_server.py` — FastMCP, port 8000, path `/mcp`
- **A2A agent:** `src/a2a_server.py` — a2a-sdk, port 9000
- **Git commits:** Single-line commit message. Never include Co-Authored-By
- **Dev docs:** Tracked in `~/projects/freelancer-on-the-build/dev/active/mcp-portfolio-server/`
