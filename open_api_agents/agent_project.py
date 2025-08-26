from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, ItemHelpers, WebSearchTool, run_demo_loop
from agents.exceptions import InputGuardrailTripwireTriggered
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from agents import function_tool
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@function_tool
def research_tool(query: str) -> str:
    """
    Search the web for information on the given query.
    """
    return "This is a research tool"

summary_agent = Agent(
    name="Summary Agent",
    instructions="You are a summary agent that can browser through the web and summarize the information.",
    tools=[
        WebSearchTool()
    ],
)

research_agent = Agent(
    name="Research Agent",
    instructions="You are a research agent that can help with any questions. Use web search tool to find the updated information. Handoff to summary agent to summarize the information.",
    tools=[
        WebSearchTool()
    ],
    handoffs=[summary_agent],
)


async def main():
    # result = Runner.run_streamed(research_agent, "What are top 3 webesites for AI related news? Get me top 10 blogs for the day related to AI from those websites")
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #         print(event.data.delta, end="", flush=True)
    # print(result.final_output)
    await run_demo_loop(research_agent)

if __name__ == "__main__":
    asyncio.run(main())


