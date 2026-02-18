PROJECTS = [
    {
        "name": "AI Receptionist Chatbot",
        "slug": "chatbot-receptionist",
        "one_liner": "Multi-agent Telegram chatbot for a dental clinic — handles bookings, FAQ, voice messages, and photos",
        "tech_stack": ["n8n", "OpenAI GPT-4", "Whisper", "Cal.com", "Supabase pgvector", "Redis", "Telegram API"],
        "problem": (
            "A dental clinic needed to handle appointment bookings, answer FAQs, "
            "and process voice/photo messages from patients — all through Telegram, "
            "24/7, without human intervention for routine requests."
        ),
        "solution": (
            "Built a multi-agent system in n8n with three specialized agents: "
            "an Intent Router that classifies incoming messages, a Booking Agent "
            "connected to Cal.com for appointment management, and a Q&A Agent "
            "with RAG over the clinic's knowledge base."
        ),
        "key_features": [
            "Multi-modal input: text, voice (Whisper transcription), and photos (GPT-4 Vision)",
            "Message buffering with Redis — aggregates rapid-fire messages before processing",
            "Intent routing: automatically directs to booking or Q&A specialist",
            "Cal.com integration: check availability, book, reschedule appointments",
            "RAG-powered Q&A: answers from clinic knowledge base via Supabase pgvector",
            "Shared PostgreSQL chat memory across all agents for conversation continuity",
        ],
        "architecture": (
            "Telegram Trigger → Normalize Input → Redis message buffer (push/get/evaluate/wait loop) "
            "→ Split by media type (voice→Whisper, photo→GPT-4V, text→passthrough) → Merge & aggregate "
            "→ Intent Router agent → [BOOKING: Cal.com tools] or [CONVERSATION: RAG vector store] "
            "→ Parse response → Loop send via Telegram with delays"
        ),
    },
    {
        "name": "Personal Finance AI Agent",
        "slug": "finance-agent",
        "one_liner": "LangGraph-powered financial assistant with real bank data, multi-turn conversation, and persistent memory",
        "tech_stack": ["LangGraph", "Python", "Anthropic Claude", "Gradio", "PostgreSQL"],
        "problem": (
            "Personal finance tracking is tedious — switching between bank apps, "
            "spreadsheets, and calculators. Needed an AI assistant that understands "
            "your actual financial data and can answer questions conversationally."
        ),
        "solution": (
            "Built a LangGraph agent that connects to real bank transaction data, "
            "maintains persistent conversation memory, and provides financial insights "
            "through a Gradio chat interface. Uses Claude as the reasoning engine "
            "with custom tools for querying and analyzing transaction history."
        ),
        "key_features": [
            "LangGraph state machine with tool-calling and multi-turn memory",
            "Real bank data integration — not mock data",
            "Custom financial analysis tools (spending by category, trends, summaries)",
            "Gradio web interface for interactive chat",
            "Persistent PostgreSQL conversation memory across sessions",
        ],
        "architecture": (
            "Gradio UI → LangGraph agent (Claude) → Tool router "
            "→ [Query transactions / Analyze spending / Summarize] "
            "→ PostgreSQL for data + chat memory → Response to UI"
        ),
    },
    {
        "name": "MCP Portfolio Server",
        "slug": "mcp-portfolio",
        "one_liner": "This server — a deployed MCP server that lets clients query my portfolio from their preferred LLM",
        "tech_stack": ["FastMCP", "Python", "Streamable HTTP", "Railway"],
        "problem": (
            "Traditional portfolios are static — clients read a page and move on. "
            "I wanted potential clients to interact with my portfolio using their "
            "own AI tools, asking specific questions relevant to their needs."
        ),
        "solution": (
            "Built a FastMCP server deployed as a public Streamable HTTP endpoint. "
            "Clients add one URL to their MCP-compatible tool (Claude Desktop, Cursor, etc.) "
            "and can ask questions about my skills, projects, services, and availability. "
            "The medium demonstrates the skill being sold."
        ),
        "key_features": [
            "Zero-friction connection — just paste a URL",
            "Works with any MCP-compatible client (Claude Desktop, Cursor, Claude Code, etc.)",
            "Structured data: skills by category, project deep-dives, service descriptions",
            "Deployed and publicly accessible 24/7",
            "The server itself is a portfolio piece demonstrating MCP expertise",
        ],
        "architecture": (
            "Client's LLM → Streamable HTTP → FastMCP server → "
            "Tool dispatcher → Structured content from data modules → Response"
        ),
    },
]
