import logging
import sys
from typing import AsyncGenerator

# 1. Add logging so you can see what fails in Logs Explorer
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

try:
    from google.adk.agents.llm_agent import LlmAgent
    from google.adk.tools.google_search_tool import GoogleSearchTool
    from google.adk.runners import InMemoryRunner
    from google.genai import types
    logger.info("ADK and GenAI libraries loaded successfully.")
except ImportError as e:
    logger.error(f"Critical Import Error: {e}")
    raise

class SearchAgent:
    def __init__(self):
        logger.info("Initializing SearchAgent...")
        # Define the agent logic
        self.adk_agent = LlmAgent(
            model="gemini-2.0-flash",
            name="google_search_agent",
            instruction="You are a helpful assistant. Use Google Search for facts.",
            tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
        )
        # Use InMemoryRunner: it handles its own session and app_name automatically
        self.runner = InMemoryRunner(agent=self.adk_agent)
        logger.info("SearchAgent ready.")

    async def query(self, input: str) -> str:
        """Endpoint for POST /api/reasoning_engine"""
        logger.info(f"Query: {input}")
        response_text = ""
        # Create a fresh message object
        content = types.UserContent(parts=[types.Part(text=input)])
        
        async for event in self.runner.run_async(user_id="user", session_id="default", new_message=content):
            if event.content and event.content.parts:
                response_text += "".join(p.text for p in event.content.parts if p.text)
        return response_text

    async def stream_query(self, input: str) -> AsyncGenerator[str, None]:
        """Endpoint for POST /api/stream_reasoning_engine"""
        logger.info(f"Streaming Query: {input}")
        content = types.UserContent(parts=[types.Part(text=input)])
        
        async for event in self.runner.run_async(user_id="user", session_id="default", new_message=content):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text

# THE ENTRYPOINT
root_agent = SearchAgent()
