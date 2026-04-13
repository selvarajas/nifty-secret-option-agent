from google.adk import Agent

from .tools import fetch_india_vix
from .prompts import VIX_SYSTEM_PROMPT

vix_agent = Agent(
    name="VixRegimeAgent",
    model="gemini-2.0-flash-exp",
    system_prompt=VIX_SYSTEM_PROMPT,
    tools=[{"name": "get_vix", "fn": fetch_india_vix}],
    temperature=0.0
)