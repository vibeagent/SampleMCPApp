import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, server_script_path: str):
        """
        Initializes the MCP Client.
        :param server_script_path: Path to the MCPServer.py script.
        """
        self.server_script_path = server_script_path
        self._session: Optional[ClientSession] = None
        self._exit_stack = AsyncExitStack()

    async def connect(self):
        """Connects to the local MCP server via stdio."""
        server_params = StdioServerParameters(
            command="python3",  # Note: ensure this environment has python 3.10+ and mcp installed
            args=[self.server_script_path],
            env=None
        )

        stdio_transport = await self._exit_stack.enter_async_context(stdio_client(server_params))
        self._stdio, self._write = stdio_transport
        
        # Connect the session
        self._session = await self._exit_stack.enter_async_context(ClientSession(self._stdio, self._write))
        await self._session.initialize()
        print("Connected to MCP Server.", flush=True)

    async def list_directory(self, path: str) -> str:
        """Calls the list_directory tool on the MCP server."""
        if not self._session:
            raise RuntimeError("Client is not connected. Call connect() first.")

        # the tool call
        result = await self._session.call_tool("list_directory", arguments={"path": path})
        
        # In Python SDK, the tool returns a list of CallToolResult objects which have content blocks
        if result and hasattr(result, "content") and isinstance(result.content, list) and len(result.content) > 0:
            return result.content[0].text
        
        return "No results."

    async def close(self):
        """Closes the connection to the MCP server."""
        await self._exit_stack.aclose()


# For basic standalone testing
async def main():
    client = MCPClient("MCPServer.py")
    try:
        await client.connect()
        # Test reading the current directory
        path = "."
        print(f"Calling list_directory for: {path}")
        result = await client.list_directory(path)
        print("\n--- Result ---")
        print(result)
        print("--------------")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
