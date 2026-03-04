from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool

google_seacrh_agent_google_search_agent = LlmAgent(
  name='Google_seacrh_agent_google_search_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
root_agent = LlmAgent(
  name='Google_seacrh_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent to help interact with my data.'
  ),
  sub_agents=[],
  instruction='',
  tools=[
    agent_tool.AgentTool(agent=google_seacrh_agent_google_search_agent)
  ],
)