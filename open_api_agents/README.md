### This is about OpenAI agent SDK

1. Agents will be designed based on their task to be achieved.
2. You can use an agent to direct the query across agents available based on the context of the query
3. GuardRail helps you block irrelevant input queries that are not supposed to be processed. You will define a funciton to undestand this. Use pydatnic model to define the output structure and the use them in the async function for validation. You can have GuardRails for both input and ouput. This helps you in raising an exception in cases of malicious usage.
4. Tools let agents take actions: things like fetching data, running code, calling external APIs, and even using a computer. There are three classes of tools in the Agent SDK:

- Hosted tools: these run on LLM servers alongside the AI models. OpenAI offers retrieval, web search and computer use as hosted tools.
- Function calling: these allow you to use any Python function as a tool.
- Agents as tools: this allows you to use an agent as a tool, allowing Agents to call other agents without handing off to them.

5. When the task is handedoff to an agent, the next query will be processed by that agent. If we use the agents as tools, everytime it will go back to the primary agent to start the workflow.

