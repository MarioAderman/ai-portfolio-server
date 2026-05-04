import asyncio
import logging

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s [server] %(message)s")
logger = logging.getLogger(__name__)

from src.mcp_server import app as mcp_app
from src.a2a_server import app as a2a_app


class _Dispatcher:
    """Routes /health inline, /mcp* to MCP, everything else to A2A. No path stripping."""

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            await self._lifespan(scope, receive, send)
            return

        path = scope.get("path", "")
        if path == "/health":
            await JSONResponse({"status": "ok"})(scope, receive, send)
        elif path.startswith("/mcp"):
            await mcp_app(scope, receive, send)
        else:
            await a2a_app(scope, receive, send)

    async def _lifespan(self, scope, receive, send):
        # FastMCP's session manager requires the lifespan to be forwarded —
        # without it, the internal task group never initialises and all MCP
        # requests fail with "Task group is not initialized".
        to_mcp: asyncio.Queue = asyncio.Queue()
        from_mcp: asyncio.Queue = asyncio.Queue()

        async def mcp_receive():
            return await to_mcp.get()

        async def mcp_send(msg):
            await from_mcp.put(msg)

        mcp_task = asyncio.create_task(mcp_app(scope, mcp_receive, mcp_send))

        startup = await receive()
        await to_mcp.put(startup)
        mcp_result = await from_mcp.get()

        if mcp_result.get("type") == "lifespan.startup.failed":
            await send(mcp_result)
            await mcp_task
            return

        logger.info("Portfolio server started (MCP + A2A)")
        await send({"type": "lifespan.startup.complete"})

        shutdown = await receive()
        await to_mcp.put(shutdown)
        await from_mcp.get()  # lifespan.shutdown.complete
        await mcp_task
        await send({"type": "lifespan.shutdown.complete"})


app = CORSMiddleware(
    _Dispatcher(),
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
