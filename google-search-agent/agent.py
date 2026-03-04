# agent.py
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

# Define the root agent with Google Search grounding
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="google_search_agent",
    description="An agent that can search the web to answer questions.",
    instruction="""
        You are a helpful research assistant. 
        Always use the Google Search tool to find the most up-to-date information before answering.
    """,
    # bypass_multi_tools_limit=True is required if you add more tools here
    tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
)
