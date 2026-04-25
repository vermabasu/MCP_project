from mcp.server.fastmcp import FastMCP
import httpx
from typing import Any
import sys

mcp = FastMCP("mcp-waether-server",
            host="0.0.0.0",
            port=8000,)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
        """

@mcp.tool()
async def get_weather(state: str) -> str:
    """Answer the weather information for a given state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


if __name__ == "__main__":
    import logging
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    
    if transport == "stdio":
        print("Running MCP server on stdio transport...", file=sys.stderr)
        sys.stderr.flush()
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running MCP server on sse transport on http://0.0.0.0:8000", file=sys.stderr)
        sys.stderr.flush()
        mcp.run(transport="sse")
    else:
        print("Invalid transport. Please choose from stdio or sse.", file=sys.stderr)
        sys.exit(1)