import asyncio
from typing import AsyncGenerator
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.runners import InMemoryRunner  # Change: Import InMemoryRunner
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
        # 2. Use InMemoryRunner to avoid manual service management
        self.runner = InMemoryRunner(agent=self.adk_agent)

    async def query(self, input: str) -> str:
        """Standard non-streaming endpoint: POST /api/reasoning_engine"""
        response_text = ""
        # Use the runner to handle the context and session logic
        async for event in self.runner.run_async(
            user_id="user", 
            session_id="default", 
            new_message=types.UserContent(parts=[types.Part(text=input)])
        ):
            if event.content and event.content.parts:
                response_text += "".join(p.text for p in event.content.parts if p.text)
        return response_text

    async def stream_query(self, input: str) -> AsyncGenerator[str, None]:
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

# Use exactly 'root_agent' to match your latest Terraform entrypoint_object
root_agent = SearchAgent()
