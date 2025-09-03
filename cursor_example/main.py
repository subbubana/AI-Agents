import asyncio
import os
import shutil
from agents import SQLiteSession
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt = """You are an expert AI assistant with full access to the filesystem directory exposed by the MCP server.

- Your job is to assist the user by reading, creating, updating, and deleting files and folders on demand.
- For any user query about existing files, base your answers strictly on those file contents.
- Always use safe, correct operations to create files or modify content exactly as the user requests.
- When creating new files, choose meaningful file names reflecting the content.
- Confirm each file operation with a brief summary of what you did.
- If uncertain about what to do with a file or folder, ask for clarification before proceeding.
- Avoid making up information beyond the files you can access.

Follow these steps for every user request: analyze intent, perform needed file operations, summarize your actions, and answer the user's questions accordingly.
"""
async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions=prompt,
        mcp_servers=[mcp_server],
    )
    session = SQLiteSession("MCP_session", "mcp_session.db")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        result = await Runner.run(starting_agent=agent, input=user_input, session=session)
        print(result.final_output)

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Filesystem Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    # Make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")

    asyncio.run(main())