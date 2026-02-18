import logging

from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [MCP] %(message)s")
logger = logging.getLogger(__name__)

from src.data.about import ABOUT
from src.data.skills import SKILLS
from src.data.services import SERVICES, PRICING
from src.data.projects import PROJECTS
from src.data.experience import EXPERIENCE
from src.data.contact import CONTACT

mcp = FastMCP(
    "Mario Aderman — AI Automation Engineer",
    instructions=(
        "You are connected to Mario Aderman's portfolio MCP server. "
        "Use the available tools to answer questions about his experience, "
        "skills, projects, services, and how to hire him. "
        "Be helpful and accurate — only share what the tools return."
    ),
)


@mcp.tool()
def get_about_me() -> dict:
    """Get Mario's professional bio, background, timezone, and availability."""
    logger.info("Tool called: get_about_me")
    return ABOUT


@mcp.tool()
def get_skills(category: str = "all") -> dict:
    """Get Mario's technical skills, optionally filtered by category.

    Args:
        category: Filter by category. Options: 'ai', 'automation', 'backend', 'frontend', 'all'.
    """
    logger.info("Tool called: get_skills(category=%s)", category)
    if category == "all":
        return SKILLS
    if category in SKILLS:
        return {category: SKILLS[category]}
    return {"error": f"Unknown category '{category}'. Options: ai, automation, backend, frontend, all"}


@mcp.tool()
def get_services() -> dict:
    """Get the services Mario offers and his pricing approach."""
    logger.info("Tool called: get_services")
    return {"services": SERVICES, "pricing": PRICING}


@mcp.tool()
def get_projects() -> list[dict]:
    """Get a summary list of all portfolio projects."""
    logger.info("Tool called: get_projects")
    return [
        {"name": p["name"], "one_liner": p["one_liner"], "tech_stack": p["tech_stack"]}
        for p in PROJECTS
    ]


@mcp.tool()
def get_project_detail(project_name: str) -> dict:
    """Get a detailed deep-dive on a specific portfolio project.

    Args:
        project_name: The project name or slug. Use get_projects() first to see available projects.
    """
    logger.info("Tool called: get_project_detail(project_name=%s)", project_name)
    query = project_name.lower()
    for project in PROJECTS:
        if query in project["name"].lower() or query in project["slug"]:
            return project
    return {
        "error": f"Project '{project_name}' not found.",
        "available": [p["name"] for p in PROJECTS],
    }


@mcp.tool()
def get_experience() -> dict:
    """Get Mario's professional experience timeline and education."""
    logger.info("Tool called: get_experience")
    return EXPERIENCE


@mcp.tool()
def get_contact_info() -> dict:
    """Get contact information, availability, and how to hire Mario."""
    logger.info("Tool called: get_contact_info")
    return CONTACT


# ASGI app for production deployment
app = mcp.http_app(path="/mcp")

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
