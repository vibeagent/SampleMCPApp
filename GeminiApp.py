import asyncio
import os
import sys
import google.genai as genai
from MCPClient import MCPClient

GEMINI_MODEL = "gemini-2.5-flash"
MCP_SERVER_SCRIPT = "MCPServer.py"

async def main():
    # 1. Setup Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set it using: export GEMINI_API_KEY='your_api_key'")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)

    # 2. Get the directory path from the user (or use current directory)
    path_to_read = input("Enter the path to read (default is '.'): ").strip()
    if not path_to_read:
         path_to_read = "."

    # 3. Read the directory using MCP
    print(f"\n--- 1. Connecting to MCP Server and reading '{path_to_read}' ---")
    client = MCPClient(MCP_SERVER_SCRIPT)
    try:
        await client.connect()
        directory_contents = await client.list_directory(path_to_read)
        print("Successfully read directory contents using MCP.")
    except Exception as e:
        print(f"Failed to read directory via MCP: {e}")
        return
    finally:
         await client.close()

    if "Error" in directory_contents:
        print(directory_contents)
        return

    # 4. Ask Gemini to analyze the contents
    print("\n--- 2. Asking Gemini to analyze the directory contents ---")
    prompt = f"""
I have a folder at path '{path_to_read}'. Here are its contents:

{directory_contents}

Could you act as a senior software engineer and briefly analyze these contents?
What kind of project does this look like? Are there any notable files or missing standard files?
Please be concise.
"""
    try:
        response = model.generate_content(prompt)
        print("\n--- Gemini's Analysis ---")
        print(response.text)
        print("-------------------------")
    except Exception as e:
         print(f"Error calling Gemini: {e}")

if __name__ == "__main__":
    asyncio.run(main())
