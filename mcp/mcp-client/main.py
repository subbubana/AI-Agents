# import asyncio
# from typing import Optional
# from contextlib import AsyncExitStack

# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
# import os
# # from anthropic import Anthropic
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()  # load environment variables from .env

# class MCPClient:
#     def __init__(self):
#         # Initialize session and client objects
#         self.session: Optional[ClientSession] = None
#         self.exit_stack = AsyncExitStack()
#         # self.anthropic = Anthropic()
#         genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         self.gemini = genai.GenerativeModel("gemini-1.5-flash")

#     async def connect_to_server(self, server_script_path: str):
#         """Connect to an MCP server
        
#         Args:
#             server_script_path: Path to the server script (.py or .js)
#         """
#         is_python = server_script_path.endswith('.py')
#         is_js = server_script_path.endswith('.js')
#         if not (is_python or is_js):
#             raise ValueError("Server script must be a .py or .js file")
            
#         command = "python" if is_python else "node"
#         server_params = StdioServerParameters(
#             command=command,
#             args=[server_script_path],
#             env=None
#         )
        
#         stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
#         self.stdio, self.write = stdio_transport
#         self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
#         await self.session.initialize()
        
#         # List available tools
#         response = await self.session.list_tools()
#         tools = response.tools
#         print("\nConnected to server with tools:", [tool.name for tool in tools])

#     async def process_query(self, query: str) -> str:
#         """Process a query using Gemini and available tools"""
#         messages = [
#             {"role": "user", "parts": [query]}
#         ]

#         # Gemini does not natively support tool-calling like Claude, so you may need to handle tool calls manually.
#         # For now, just send the user query to Gemini and return the response.

#         response = self.gemini.generate_content(messages)
#         return response.text

#     # async def process_query(self, query: str) -> str:
#     #     """Process a query using Claude and available tools"""
#     #     messages = [
#     #         {
#     #             "role": "user",
#     #             "content": query
#     #         }
#     #     ]

#     #     response = await self.session.list_tools()
#     #     available_tools = [{ 
#     #         "name": tool.name,
#     #         "description": tool.description,
#     #         "input_schema": tool.inputSchema
#     #     } for tool in response.tools]

#     #     # Initial Claude API call
#     #     response = self.anthropic.messages.create(
#     #         model="claude-3-5-sonnet-20241022",
#     #         max_tokens=1000,
#     #         messages=messages,
#     #         tools=available_tools
#     #     )

#     #     # Process response and handle tool calls
#     #     tool_results = []
#     #     final_text = []

#     #     for content in response.content:
#     #         if content.type == 'text':
#     #             final_text.append(content.text)
#     #         elif content.type == 'tool_use':
#     #             tool_name = content.name
#     #             tool_args = content.input
                
#     #             # Execute tool call
#     #             result = await self.session.call_tool(tool_name, tool_args)
#     #             tool_results.append({"call": tool_name, "result": result})
#     #             final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

#     #             # Continue conversation with tool results
#     #             if hasattr(content, 'text') and content.text:
#     #                 messages.append({
#     #                   "role": "assistant",
#     #                   "content": content.text
#     #                 })
#     #             messages.append({
#     #                 "role": "user", 
#     #                 "content": result.content
#     #             })

#     #             # Get next response from Claude
#     #             response = self.anthropic.messages.create(
#     #                 model="claude-3-5-sonnet-20241022",
#     #                 max_tokens=1000,
#     #                 messages=messages,
#     #             )

#     #             final_text.append(response.content[0].text)

#     #     return "\n".join(final_text)

#     async def chat_loop(self):
#         """Run an interactive chat loop"""
#         print("\nMCP Client Started!")
#         print("Type your queries or 'quit' to exit.")
        
#         while True:
#             try:
#                 query = input("\nQuery: ").strip()
                
#                 if query.lower() == 'quit':
#                     break
                    
#                 response = await self.process_query(query)
#                 print("\n" + response)
                    
#             except Exception as e:
#                 print(f"\nError: {str(e)}")
    
#     async def cleanup(self):
#         """Clean up resources"""
#         await self.exit_stack.aclose()

# async def main():
#     if len(sys.argv) < 2:
#         print("Usage: python client.py <path_to_server_script>")
#         sys.exit(1)
        
#     client = MCPClient()
#     try:
#         await client.connect_to_server(sys.argv[1])
#         await client.chat_loop()
#     finally:
#         await client.cleanup()

# if __name__ == "__main__":
#     import sys
#     asyncio.run(main())

# client.py

import asyncio
import sys
from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client
import os
import google.generativeai as genai
from google.generativeai.types import Tool as GeminiTool, FunctionDeclaration
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

# Add this function at the top-level (after imports)
def remove_titles_from_schema(schema):
    if isinstance(schema, dict):
        return {k: remove_titles_from_schema(v) for k, v in schema.items() if k != "title"}
    elif isinstance(schema, list):
        return [remove_titles_from_schema(item) for item in schema]
    return schema

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.gemini_tools: Optional[GeminiTool] = None
        self.exit_stack = AsyncExitStack()
        
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # Set enable_automatic_function_calling to False to manually control the loop
        self.gemini = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"temperature": 0}
        )
        self.chat = self.gemini.start_chat(enable_automatic_function_calling=False)


    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server and translate its tools for Gemini."""
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # --- Start of Adapter Logic ---
        # 1. Fetch tools from the MCP server
        response = await self.session.list_tools()
        mcp_tools: List[Tool] = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in mcp_tools])

        # 2. Translate MCP tools into Gemini's format
        declarations = []
        for tool in mcp_tools:
            # The MCP `inputSchema` is a JSON Schema, which is what Gemini needs.
            clean_schema = remove_titles_from_schema(tool.inputSchema)
            declaration = FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=clean_schema
            )
            declarations.append(declaration)
        
        # Store as a single Tool object for the Gemini API
        self.gemini_tools = GeminiTool(function_declarations=declarations)
        # --- End of Adapter Logic ---

    async def process_query(self, query: str) -> str:
        """
        Process a query using Gemini and a given conversation history.
        NOTE: This function no longer uses 'self.history'.
        """
        history = []
        if not self.session or not self.gemini_tools:
            return "Client not connected or tools not initialized."

        # Add the user's new message to the local history for this turn
        history.append({"role": "user", "parts": [{"text": query}]})

        # Loop to handle potential multi-turn tool calls
        while True:
            response = self.gemini.generate_content(history, tools=[self.gemini_tools])
            candidate = response.candidates[0]
            
            # If there's no function call, we have the final answer.
            if not candidate.content.parts or not candidate.content.parts[0].function_call.name:
                final_text = "".join(part.text for part in candidate.content.parts if part.text)
                history.append({"role": "model", "parts": [{"text": final_text}]})
                return final_text

            # It's a tool call, so add the model's request to history and execute.
            history.append(candidate.content)
            
            function_call = candidate.content.parts[0].function_call
            tool_name = function_call.name
            tool_args = {key: value for key, value in function_call.args.items()}
            
            print(f"🤖 Gemini wants to call tool: {tool_name} with args: {tool_args}")
            
            tool_result = await self.session.call_tool(tool_name, tool_args)
            
            # Add the tool's result to history for the next loop iteration.
            history.append({
                "role": "tool",
                "parts": [{
                    "function_response": {
                        "name": tool_name,
                        "response": {"result": tool_result.content},
                    }
                }]
            })

    async def chat_loop(self):
        """Run an interactive chat loop."""
        print("\n🤖 Gemini MCP Client Started!")
        print("Ask me for a weather forecast or alerts. Type 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        print("\nCleaning up and shutting down...")
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())