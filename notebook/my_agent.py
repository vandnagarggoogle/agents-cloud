from google.adk.agents import Agent
from google.adk.integrations.agent_registry import AgentRegistry
from vertexai.agent_engines import AdkApp
import os

# Initialize the Agent Registry client
registry = AgentRegistry(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="global"
)

# CORRECTED: Use get_mcp_toolset with the full resource name of the BigQuery MCP server
# This replaces the failing 'registry.mcpServers.get' call
bq_tools = registry.get_mcp_toolset(
    "projects/f7-aesthetic-frame-479413/locations/global/mcpServers/agentregistry-00000000-0000-0000-308e-18597b8ca588"
)

# Define the Agent logic
root_agent = Agent(
    model='gemini-2.0-flash',
    name='bigquery-assistant',
    instruction="You are a BigQuery expert. Use tools to query data and summarize results.",
    tools=[bq_tools],
)

# Wrap the agent in AdkApp
agent = AdkApp(agent=root_agent)
