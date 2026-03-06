import json
import logging
import os
import uuid

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [A2A] %(message)s")
logger = logging.getLogger(__name__)
from groq import Groq

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    Message,
    Part,
    TextPart,
)

from src.data.about import ABOUT
from src.data.skills import SKILLS
from src.data.services import SERVICES, PRICING
from src.data.projects import PROJECTS
from src.data.experience import EXPERIENCE
from src.data.contact import CONTACT

load_dotenv()

PORTFOLIO_CONTEXT = f"""You are Mario Aderman's portfolio agent — "Have You Met Mario?"
You answer questions about Mario's professional background, skills, projects, and services.
Be conversational, helpful, and concise. Only share information from the context below.
If asked something not covered, say you don't have that information and suggest contacting Mario on Upwork.

=== ABOUT ===
{json.dumps(ABOUT, indent=2)}

=== SKILLS ===
{json.dumps(SKILLS, indent=2)}

=== SERVICES ===
{json.dumps(SERVICES, indent=2)}

=== PRICING ===
{json.dumps(PRICING, indent=2)}

=== PROJECTS ===
{json.dumps(PROJECTS, indent=2)}

=== EXPERIENCE ===
{json.dumps(EXPERIENCE, indent=2)}

=== CONTACT ===
{json.dumps(CONTACT, indent=2)}
"""

GROQ_MODEL = "llama-3.1-8b-instant"


def _extract_text(message) -> str:
    """Extract plain text from an A2A Message."""
    texts = []
    for part in message.parts or []:
        if hasattr(part, "root") and hasattr(part.root, "text"):
            texts.append(part.root.text)
        elif hasattr(part, "text"):
            texts.append(part.text)
    return " ".join(texts)


def get_llm_response(conversation: list[dict[str, str]]) -> str:
    logger.info("LLM request: model=%s, turns=%d", GROQ_MODEL, len(conversation))
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        messages = [{"role": "system", "content": PORTFOLIO_CONTEXT}] + conversation
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
        answer = response.choices[0].message.content
        logger.info("LLM response: %d chars", len(answer))
        return answer
    except Exception as e:
        logger.error("LLM call failed: %s", e)
        return "Sorry, I'm having trouble processing your request right now. Please try again or contact Mario directly on Upwork."


class PortfolioAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        # Build conversation history from previous task messages
        conversation: list[dict[str, str]] = []
        if context.task and context.task.history:
            for msg in context.task.history:
                role = "assistant" if msg.role == "agent" else "user"
                text = _extract_text(msg)
                if text:
                    conversation.append({"role": role, "content": text})

        # Add current message
        user_message = _extract_text(context.message) if context.message else ""
        if not user_message:
            user_message = "Tell me about yourself"
        conversation.append({"role": "user", "content": user_message})

        logger.info("Incoming message: '%s' (history: %d turns)", user_message[:150], len(conversation) - 1)
        response_text = get_llm_response(conversation)

        message = Message(
            role="agent",
            messageId=str(uuid.uuid4()),
            parts=[Part(root=TextPart(text=response_text))],
        )
        await event_queue.enqueue_event(message)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass


agent_card = AgentCard(
    name="Have You Met Mario? — AI Automation Engineer",
    description=(
        "Mario Aderman's portfolio agent. Ask about his experience, skills, "
        "projects, services, and availability for AI automation work."
    ),
    version="1.0.0",
    url="https://agent.fintegra.solutions/",
    defaultInputModes=["text/plain"],
    defaultOutputModes=["text/plain"],
    capabilities=AgentCapabilities(streaming=False, pushNotifications=False),
    skills=[
        AgentSkill(
            id="portfolio_query",
            name="Portfolio Query",
            description="Get information about Mario's past AI automation projects and case studies",
            tags=["portfolio", "projects", "AI automation", "n8n", "LangChain"],
            examples=[
                "What projects have you built?",
                "Tell me about the chatbot project",
                "What's your tech stack?",
            ],
        ),
        AgentSkill(
            id="service_inquiry",
            name="Service Inquiry",
            description="Learn about Mario's services, rates, and engagement approach",
            tags=["services", "rates", "pricing", "freelance"],
            examples=[
                "What services do you offer?",
                "How much do you charge?",
                "Do you work with n8n?",
            ],
        ),
        AgentSkill(
            id="availability_check",
            name="Availability Check",
            description="Check Mario's current availability and how to hire him",
            tags=["availability", "hiring", "contact", "Upwork"],
            examples=[
                "Are you available for a project?",
                "How do I hire you?",
                "What's your timezone?",
            ],
        ),
    ],
)

task_store = InMemoryTaskStore()
agent_executor = PortfolioAgentExecutor()
request_handler = DefaultRequestHandler(
    agent_executor=agent_executor,
    task_store=task_store,
)

a2a_app = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

app = a2a_app.build()

from starlette.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
