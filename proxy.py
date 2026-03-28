"""
Minimal MCP stdio proxy that forwards all requests to the remote Nefesh MCP server.
Used by Glama.ai for server inspection and tool detection.
"""
import os
import httpx
from mcp.server.fastmcp import FastMCP

REMOTE_URL = "https://mcp.nefesh.ai/mcp"
API_KEY = os.environ.get("NEFESH_API_KEY", "")

mcp = FastMCP("nefesh-proxy")


async def _call_remote(method: str, params: dict) -> dict:
    """Forward a JSON-RPC call to the remote MCP server."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            REMOTE_URL,
            json={"jsonrpc": "2.0", "method": method, "params": params, "id": 1},
            headers={
                "X-Nefesh-Key": API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )
        data = resp.json()
        return data.get("result", data)


@mcp.tool()
async def ingest_signal(
    session_id: str,
    heart_rate: float = 0,
    rmssd: float = 0,
    sdnn: float = 0,
    respiratory_rate: float = 0,
    spo2: float = 0,
    systolic_bp: float = 0,
    diastolic_bp: float = 0,
    skin_temperature: float = 0,
    gsr: float = 0,
    vocal_pitch_mean: float = 0,
    vocal_energy: float = 0,
    speech_rate: float = 0,
    facial_valence: float = 0,
    facial_arousal: float = 0,
    au4_brow_lowerer: float = 0,
    blink_rate: float = 0,
    gaze_stability: float = 0,
    text_content: str = "",
    text_sentiment: float = 0,
    timestamp: str = "",
) -> dict:
    """Send raw sensor data to Nefesh and receive a unified stress score (0-100)."""
    params = {k: v for k, v in locals().items() if v}
    return await _call_remote("tools/call", {"name": "ingest_signal", "arguments": params})


@mcp.tool()
async def get_human_state(session_id: str) -> dict:
    """Get the current physiological state for a session."""
    return await _call_remote("tools/call", {"name": "get_human_state", "arguments": {"session_id": session_id}})


@mcp.tool()
async def get_history(session_id: str, minutes: int = 5) -> dict:
    """Get state history over time for a session."""
    return await _call_remote("tools/call", {"name": "get_history", "arguments": {"session_id": session_id, "minutes": minutes}})


@mcp.tool()
async def delete_subject(subject_id: str) -> dict:
    """GDPR-compliant deletion of all data for a subject."""
    return await _call_remote("tools/call", {"name": "delete_subject", "arguments": {"subject_id": subject_id}})


if __name__ == "__main__":
    mcp.run(transport="stdio")
