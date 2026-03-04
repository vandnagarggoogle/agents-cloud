import logging
from typing import AsyncGenerator
from google.adk.agents import Agent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from google.adk.runners import InMemoryRunner
from google.genai import types

# --- PROMPTS ---
DATA_ANALYST_PROMPT = "Generate a comprehensive market analysis report for a provided_ticker using Google Search. Focus on SEC filings, news, and sentiment."
TRADING_ANALYST_PROMPT = "Conceptualize 5 distinct trading strategies based on market_data_analysis_output, risk attitude, and investment period."
EXECUTION_ANALYST_PROMPT = "Generate a detailed execution plan (entry, hold, exit) for the provided trading strategies."
RISK_ANALYST_PROMPT = "Provide a final risk assessment of the entire financial plan, checking alignment with user risk profile."
COORDINATOR_PROMPT = """
Role: Specialized financial advisory assistant. 
Introduction: "Hello! I'm here to help you navigate financial decision-making."
Process:
1. Gather Ticker -> Call data_analyst.
2. Ask Risk/Period -> Call trading_analyst.
3. Call execution_analyst.
4. Call risk_analyst for final report.
"""

# --- SUB-AGENTS ---
data_analyst = Agent(
    name="data_analyst",
    instruction=DATA_ANALYST_PROMPT,
    tools=[google_search],
    output_key="market_data_analysis_output"
)

trading_analyst = Agent(
    name="trading_analyst",
    instruction=TRADING_ANALYST_PROMPT,
    output_key="proposed_trading_strategies_output"
)

execution_analyst = Agent(
    name="execution_analyst",
    instruction=EXECUTION_ANALYST_PROMPT,
    output_key="execution_plan_output"
)

risk_analyst = Agent(
    name="risk_analyst",
    instruction=RISK_ANALYST_PROMPT,
    output_key="final_risk_assessment_output"
)

# --- COORDINATOR (ROOT) ---
financial_coordinator = LlmAgent(
    name="financial_coordinator",
    model="gemini-2.0-flash",
    description="Orchestrates financial experts to provide comprehensive advice.",
    instruction=COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=data_analyst),
        AgentTool(agent=trading_analyst),
        AgentTool(agent=execution_analyst),
        AgentTool(agent=risk_analyst),
    ],
)

# --- WRAPPER FOR REASONING ENGINE ---
class FinancialAdvisorAgent:
    def __init__(self):
        self.runner = InMemoryRunner(agent=financial_coordinator)

    async def query(self, input: str) -> str:
        response_text = ""
        content = types.UserContent(parts=[types.Part(text=input)])
        async for event in self.runner.run_async(user_id="user", session_id="default", new_message=content):
            if event.content and event.content.parts:
                response_text += "".join(p.text for p in event.content.parts if p.text)
        return response_text

    async def async_stream_query(self, input: str) -> AsyncGenerator[str, None]:
        content = types.UserContent(parts=[types.Part(text=input)])
        async for event in self.runner.run_async(user_id="user", session_id="default", new_message=content):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text

root_agent = FinancialAdvisorAgent()
