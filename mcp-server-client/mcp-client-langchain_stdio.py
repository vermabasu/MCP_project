import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Optional, List, Dict, Any


class MCPClientStdio:
    """MCP Client using Stdio transport"""
    
    def __init__(self, server_script: str = "mcp-server.py"):
        self.server_script = server_script
        self.session: Optional[ClientSession] = None
        self.tools: List[Dict[str, Any]] = []
    
    async def connect(self) -> bool:
        """Connect to the MCP server via Stdio"""
        try:
            server_params = StdioServerParameters(
                command="python",
                args=[self.server_script],
            )
            
            self.read_stream, self.write_stream = await stdio_client(server_params).__aenter__()
            self.session = ClientSession(self.read_stream, self.write_stream)
            await self.session.__aenter__()
            await self.session.initialize()
            
            # Get available tools
            tools_list = await self.session.list_tools()
            self.tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                }
                for tool in tools_list.tools
            ]
            
            print(f"Connected to MCP server via stdio")
            print(f"Available tools: {[tool['name'] for tool in self.tools]}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.session:
            await self.session.__aexit__(None, None, None)
        print("Disconnected from server")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the server"""
        if not self.session:
            return "Not connected to server"
        
        try:
            result = await self.session.call_tool(tool_name, arguments=arguments)
            if result.content:
                return result.content[0].text
            return "No result"
        except Exception as e:
            return f"Error calling tool: {e}"
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        return self.tools


async def main():
    # Example usage
    client = MCPClientStdio()
    
    if await client.connect():
        # List tools
        print("\nAvailable tools:")
        for tool in client.list_tools():
            print(f"  - {tool['name']}: {tool['description']}")
        
        # Call a tool
        print("\nCalling 'add' tool with a=10, b=5:")
        result = await client.call_tool("add", {"a": 10, "b": 5})
        print(f"Result: {result}")
        
        # Call weather tool
        print("\nCalling 'get_weather' tool with state='NY':")
        result = await client.call_tool("get_weather", {"state": "NY"})
        print(f"Result: {result}")
        
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())