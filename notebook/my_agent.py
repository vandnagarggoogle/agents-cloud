from google.adk.agents import Agent
from google.adk.integrations.agent_registry import AgentRegistry
from vertexai.agent_engines import AdkApp
import os

# 1. Initialize the Agent Registry client
# This allows the agent to find tools in the registry at runtime
registry = AgentRegistry(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location=os.environ.get("GOOGLE_CLOUD_LOCATION")
)

# 2. Fetch the BigQuery tools from the registry
# Use the unique MCP ID discovered in your staging registry earlier
bq_tools = registry.mcpServers.get(
    name="agentregistry-00000000-0000-0000-308e-18597b8ca588"
)

# 3. Define the Agent logic
# We equip the agent with the bq_tools set
root_agent = Agent(
    model='gemini-2.0-flash',
    name='bigquery-assistant',
    description="An agent that queries BigQuery using MCP tools.",
    instruction="""You are a BigQuery expert. 
    Use the BigQuery tools to list datasets, find tables, and execute SQL queries.
    Always provide a clear summary of the data you find.""",
    tools=[bq_tools],
)

# 4. Wrap the agent in AdkApp
# This object 'agent' matches your 'entrypointObject' in the deployment spec
# It exposes 'query_str', 'query_dict', and other standard methods
agent = AdkApp(agent=root_agent)
