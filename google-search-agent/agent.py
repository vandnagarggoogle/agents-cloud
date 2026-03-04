import asyncio
import logging
from typing import AsyncGenerator
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.runners import InMemoryRunner
from google.genai import types

class SearchAgent:
    def __init__(self):
        # 1. Initialize the ADK agent
        self.adk_agent = LlmAgent(
            model="gemini-2.0-flash",
            name="google_search_agent",
            instruction="You are a helpful assistant. Use Google Search for facts.",
            tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
        )
        # 2. InMemoryRunner is the robust choice for custom agents
        self.runner = InMemoryRunner(agent=self.adk_agent)

    async def query(self, input: str) -> str:
        """Standard endpoint: POST /api/reasoning_engine"""
        response_text = ""
        # user_id and session_id are required by the ADK Runner
        async for event in self.runner.run_async(
            user_id="user", 
            session_id="default", 
            new_message=types.UserContent(parts=[types.Part(text=input)])
        ):
            if event.content and event.content.parts:
                response_text += "".join(p.text for p in event.content.parts if p.text)
        return response_text

    # CHANGE: Renamed from 'stream_query' to 'async_stream_query'
    async def async_stream_query(self, input: str) -> AsyncGenerator[str, None]:
        """Streaming endpoint: POST /api/stream_reasoning_engine"""
        async for event in self.runner.run_async(
            user_id="user", 
            session_id="default", 
            new_message=types.UserContent(parts=[types.Part(text=input)])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text

# THE ENTRYPOINT
root_agent = SearchAgent()
