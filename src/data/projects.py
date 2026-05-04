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
        "one_liner": "LangGraph-powered financial advisor with 9 tools, chart generation, CRUD with human-in-the-loop, and multi-provider LLM support",
        "tech_stack": ["LangGraph", "LangChain", "Python", "OpenAI", "Anthropic", "Google", "HuggingFace", "Gradio", "PostgreSQL", "matplotlib", "LangSmith"],
        "problem": (
            "Personal finance tracking is tedious — switching between bank apps, "
            "spreadsheets, and calculators. Needed an AI assistant that understands "
            "your financial data and can answer questions, generate charts, and "
            "manage transactions conversationally."
        ),
        "solution": (
            "Built a LangGraph agent with 9 specialized tools for querying, analyzing, "
            "and managing financial data through a Gradio chat interface. Supports "
            "multiple LLM providers (OpenAI, Anthropic, Google, HuggingFace) with "
            "runtime switching. Includes a demo mode with seed data for showcasing."
        ),
        "key_features": [
            "LangGraph state machine with tool-calling and multi-turn memory",
            "9 tools: SQL queries, account balances, spending by category, recent transactions, chart generation, and full CRUD",
            "Human-in-the-loop confirmation for all write operations (create, update, delete) via LangGraph interrupt()",
            "Chart generation with matplotlib — bar, pie, line, and grouped bar charts rendered inline",
            "Multi-provider LLM support with runtime switching (OpenAI, Anthropic, Google, HuggingFace)",
            "Chat history with thread resume — persistent PostgreSQL conversation memory across sessions",
            "LangSmith tracing and evaluation with custom evaluators",
        ],
        "architecture": (
            "Gradio Blocks UI → LangGraph StateGraph → agent node (multi-provider LLM) "
            "→ should_continue router → tools node (9 tools) ↔ agent → END "
            "→ PostgreSQL for financial data + checkpointer for conversation persistence "
            "→ LangSmith for tracing"
        ),
    },
    {
        "name": "AI Portfolio Server",
        "slug": "ai-portfolio",
        "one_liner": "Dual-protocol AI portfolio — MCP server for structured tool access + A2A agent for conversational discovery",
        "tech_stack": ["FastMCP", "a2a-sdk", "Python", "Streamable HTTP", "Llama 3.1 8B", "Groq", "Docker", "Render"],
        "problem": (
            "Traditional portfolios are static — clients read a page and move on. "
            "I wanted potential clients to interact with my portfolio using their "
            "own AI tools, asking specific questions relevant to their needs."
        ),
        "solution": (
            "Built a dual-protocol server: an MCP server with 7 tools for structured "
            "portfolio queries, and an A2A agent (\"Have You Met Mario?\") powered by "
            "Llama 3.1 8B via Groq for conversational agent-to-agent interaction. Both share "
            "the same data layer in a single combined service. "
            "The medium demonstrates the skill being sold."
        ),
        "key_features": [
            "MCP server: 7 tools (about, skills, services, projects, experience, contact) via Streamable HTTP",
            "A2A agent: conversational portfolio discovery using Llama 3.1 8B via Groq",
            "Shared data layer — both protocols serve the same content modules",
            "Zero-friction MCP connection — just paste a URL into any compatible client",
            "A2A Agent Card at /.well-known/agent.json for automated agent discovery",
            "Deployed on Render free tier with UptimeRobot keep-warm monitor",
            "The server itself is a portfolio piece demonstrating MCP and A2A expertise",
        ],
        "architecture": (
            "MCP path: Client LLM → Streamable HTTP → FastMCP → 7 tool handlers → shared data modules | "
            "A2A path: Other agents → JSON-RPC 2.0 → a2a-sdk → Llama 3.1 8B (Groq) → shared data modules"
        ),
    },
    {
        "name": "AgriScore",
        "slug": "agriscore",
        "one_liner": "Cloud-native agricultural credit scoring platform using satellite data, Claude AI agent, and ML — Top 4 at Talent Land 2026",
        "tech_stack": ["Python", "FastAPI", "Next.js", "TypeScript", "AWS Fargate", "AWS Lambda", "Step Functions", "Claude (tool-use)", "scikit-learn", "PostgreSQL", "PostGIS", "Sentinel-2", "WhatsApp"],
        "problem": (
            "Unbanked farmers in Mexico lack access to credit because they have no "
            "traditional credit bureau history. Financial institutions have no reliable "
            "way to assess their creditworthiness, leaving them excluded from formal financing."
        ),
        "solution": (
            "Built AgriScore, a cloud-native platform that generates verified agricultural "
            "credit profiles using alternative data: satellite imagery (NDVI via Sentinel-2/Copernicus), "
            "climate data (Open-Meteo, NASA POWER), socioeconomic indicators (INEGI), and "
            "AI document processing (Claude Vision). A conversational Claude agent guides "
            "farmers through onboarding via WhatsApp. A Random Forest ML model produces "
            "a credit score on a 300-850 scale."
        ),
        "key_features": [
            "Claude tool-use agent on WhatsApp — guides farmers through onboarding conversationally",
            "AWS Step Functions pipeline with 6 parallel Lambda steps: document extraction, satellite fetch, climate fetch, socioeconomic data, ML scoring, report generation",
            "Satellite NDVI analysis via Sentinel Hub (Copernicus/Sentinel-2) to assess crop health and land use",
            "Random Forest ML model trained on synthetic data — 300-850 credit score scale",
            "3 isolated Fargate services: AI agent core, REST API for financial institutions, WhatsApp bridge",
            "Next.js + TypeScript dashboard with gamification for farmers",
            "Top 4 finalist — Genius Arena @ Talent Land 2026, Capital One 'Finanzas para un Futuro Sostenible' track",
        ],
        "architecture": (
            "WhatsApp → EvolutionAPI bridge → FastAPI Core (Claude tool-use agent) → "
            "Step Functions pipeline [ExtractDocs | FetchSatellite ∥ FetchClimate ∥ FetchSocioeconomic | CalculateScore | GenerateExpediente] → "
            "PostgreSQL+PostGIS | REST API (Fargate) → Next.js dashboard | "
            "Financial institutions query via authenticated REST API"
        ),
    },
]
