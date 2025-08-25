from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, ItemHelpers
from agents.exceptions import InputGuardrailTripwireTriggered
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking valid questions.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance only with historical queries. Don't asnwer any other questions. Explain important events and context clearly.",
    handoffs=[math_tutor_agent],
    # input_guardrails=[
    #     InputGuardrail(guardrail_function=homework_guardrail),
    # ],
)



tutor_agent = Agent(
    name="Tutor Agent",
    instructions="You provide help with valid questions. Explain with detail and provide infromaiton through examples",
    # input_guardrails=[
    #     InputGuardrail(guardrail_function=homework_guardrail),
    # ],
)




triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    # input_guardrails=[
    #     InputGuardrail(guardrail_function=homework_guardrail),
    # ],
)

async def main():
    # agent = Agent(
    #     name="Joker",
    #     instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
    #     tools=[how_many_jokes],
    # )

    result = Runner.run_streamed(
        math_tutor_agent,
        input="In which year taj mahal was built and what is the sum of digits of that year?",
    )
    print("=== Run starting ===")

    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")
# async def main():
#     # Example 1: History question
#     # try:
#     #     result = await Runner.run(triage_agent, "who was the first president of the united states?")
#     #     print(result.final_output)
#     # except InputGuardrailTripwireTriggered as e:
#     #     print("Guardrail blocked this input:", e)

#     # Example 2: General/philosophical question
#     try:
#         result = Runner.run_streamed(triage_agent, "What is the formula for volume of a sphere? And what is the reason for worldwar 1?")
#         async for event in result.stream_events():
#             if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#                 print(event.data.delta, end="", flush=True)
#         # print(result.final_output)
#     except InputGuardrailTripwireTriggered as e:
#         print("Guardrail blocked this input:", e)

if __name__ == "__main__":
    asyncio.run(main())