from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP Server
mcp = FastMCP("Sample Python Local Folder Reader")

@mcp.tool()
def list_directory(path: str) -> str:
    """Lists the files and directories inside the given path."""
    try:
        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist."
        if not os.path.isdir(path):
            return f"Error: Path '{path}' is not a directory."
            
        entries = os.listdir(path)
        
        output = [f"Contents of '{path}':"]
        for entry in sorted(entries):
            full_path = os.path.join(path, entry)
            is_dir = os.path.isdir(full_path)
            prefix = "[DIR] " if is_dir else "[FILE]"
            output.append(f"{prefix} {entry}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error reading directory: {str(e)}"

if __name__ == "__main__":
    # Start the server using stdio transport
    print(f"Starting MCP Server on stdio...", file=os.sys.stderr)
    mcp.run(transport='stdio')
