# google-search-agent/agent.py
import asyncio
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.runners import InMemoryRunner

class SearchAgent:
    def __init__(self):
        # 1. Initialize the ADK agent
        self.adk_agent = LlmAgent(
            model="gemini-2.0-flash",
            name="google_search_agent",
            instruction="You are a helpful assistant. Use Google Search for facts.",
            tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
        )
        # 2. Use a Runner to handle the execution context
        self.runner = InMemoryRunner(agent=self.adk_agent)

    async def query(self, input: str) -> str:
        """
        Reasoning Engine calls this method. We use the runner to execute the agent logic.
        """
        # run_debug is a helper that returns a list of events
        events = await self.runner.run_debug(input, quiet=True)
        
        # Extract the final text from the events
        for event in reversed(events):
            if event.content and event.content.parts:
                return "".join(p.text for p in event.content.parts if p.text)
        
        return "No response generated."

# Match this to your Terraform entrypoint_object
root_agent = SearchAgent()
