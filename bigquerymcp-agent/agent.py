from google.adk.agents import Agent
from google.adk.integrations.agent_registry import AgentRegistry
from vertexai.agent_engines import AdkApp
import os

# Initialize Registry client
registry = AgentRegistry(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="global"
)

# Fetch the BigQuery tools using the staging resource ID
# Resource ID discovered from 'agent-registry mcp-servers list'
bq_resource = "projects/f7-aesthetic-frame-479413/locations/global/mcpServers/agentregistry-00000000-0000-0000-308e-18597b8ca588"
bq_tools = registry.get_mcp_toolset(bq_resource)

# Define the Data Science Agent
root_agent = Agent(
    model='gemini-2.0-flash',
    name='data-science-agent',
    instruction="""You are a world-class data scientist. 
    Use BigQuery to retrieve data and return helpful insights.""",
    tools=[bq_tools],
)

agent = AdkApp(agent=root_agent)
