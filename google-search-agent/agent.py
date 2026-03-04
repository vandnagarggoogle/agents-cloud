# google-search-agent/agent.py
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

class SearchAgent:
    def __init__(self):
        # Initialize the underlying ADK agent
        self.agent = LlmAgent(
            model="gemini-2.0-flash",
            name="google_search_agent",
            description="An agent that can search the web to answer questions.",
            instruction="""
                You are a helpful research assistant. 
                Always use the Google Search tool to find the most up-to-date information before answering.
            """,
            tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
        )

    def query(self, input: str) -> str:
        """
        Explicitly define the query method for Reasoning Engine registration.
        """
        # Call the underlying ADK agent's invocation logic
        # Note: Depending on ADK version, this might be self.agent.invoke(input) 
        # or self.agent.query(input) if using the standard LlmAgent.
        return self.agent.invoke(input) 

# Define the entrypoint object expected by your Terraform
root_agent = SearchAgent()
