from google.adk import Agent
from .strategy_engine import StrategyEngine
from .prompts import STRATEGY_SYSTEM_PROMPT

strategy_agent = Agent(
    name="StrategyDecisionAgent",
    model="gemini-2.0-flash-exp",
    system_prompt=STRATEGY_SYSTEM_PROMPT,
    tools=[{"name": "recommend_strategy", "fn": StrategyEngine.recommend}],
    temperature=0.0
)