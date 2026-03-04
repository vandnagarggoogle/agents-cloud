# agent.py
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
import google.auth

# Configuration for BigQuery MCP
BIGQUERY_AGENT_NAME = "bigquery_mcp_agent"
BIGQUERY_MCP_ENDPOINT = "https://bigquery.googleapis.com/mcp"
BIGQUERY_SCOPE = "https://www.googleapis.com/auth/bigquery"

# Initialize credentials for the MCP connection
credentials, project_id = google.auth.default(scopes=[BIGQUERY_SCOPE])
credentials.refresh(google.auth.transport.requests.Request())
oauth_token = credentials.token

# Set up the BigQuery MCP Toolset
bigquery_mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=BIGQUERY_MCP_ENDPOINT,
        headers={"Authorization": f"Bearer {oauth_token}"},
    )
)

# Define the root agent
root_agent = LlmAgent(
    model="gemini-2.0-flash", # Or your preferred model
    name=BIGQUERY_AGENT_NAME,
    description="Agent to answer questions about BigQuery data and execute SQL queries using MCP.",
    instruction="""
        You are a data science assistant. 
        Use the provided BigQuery tools to explore datasets and answer user questions with SQL.
    """,
    tools=[bigquery_mcp_toolset],
)
