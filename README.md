# Sample MCP Application with Gemini Integration

This sample demonstrates how to build and interact with a Model Context Protocol (MCP) server. 
It includes a local Python MCP server that exposes a folder-reading tool, an MCP client that connects to it, and a Gemini application that orchestrates them.

## Prerequisites

- **Python 3.10 or higher**: The official `mcp` SDK requires [Python 3.10+](https://www.python.org/downloads/).
- **Node.js & npm**: Required **only** if you want to use the `mcp dev` Inspector. It uses `@modelcontextprotocol/inspector` under the hood. 
- **Gemini API Key**: You need an API key from Google AI Studio.

## Setup

1. **Ensure Python 3.10+ is installed**: 
   Check your version with `python3 --version`.
   If you have an older version, install a newer one (e.g., via [Homebrew](https://brew.sh/) `brew install python@3.12` on Mac).

2. **Create a virtual environment (using Python 3.10+)**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install mcp httpx google-generativeai pydantic
   ```

4. **Set your API Key**:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

## Running the Applications

### 1. Test the MCP Server and Client only
You can test the base MCP Client and Server communication by running:
```bash
python MCPClient.py
```
This will launch the server in the background and list the contents of the current directory.

### 2. Run the full Gemini Application
To interact with the AI model:
```bash
python GeminiApp.py
```
1. It will prompt you for a folder path to read.
2. It fetches the contents using the MCP protocol.
3. It sends those contents to Gemini and asks for a brief analysis.
4. Gemini's response will be printed to the console.

## Files
- `MCPServer.py`: The FastMCP server implementation providing the `list_directory` tool.
- `MCPClient.py`: The client script that connects to the server and calls the tool.
- `GeminiApp.py`: The application integrating the MCPClient and the Gemini API.
