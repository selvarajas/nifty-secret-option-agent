from .vix_agent import vix_agent
from .strategy_agent import strategy_agent
from .tools import fetch_india_vix, fetch_nifty_option_chain, fetch_nifty_volume_profile
from .analyzers import analyze_pcr
from .strategy_engine import StrategyEngine
from .prompts import SYSTEM_PROMPT

# Root Agent (this is what ADK looks for)
root_agent = Orchestrator(
    name="NiftySecretOptionOrchestrator",
    agents=[vix_agent, strategy_agent],
    model="gemini-2.0-flash-exp",   # or gemini-1.5-pro / gemini-2.5-flash
    system_prompt=SYSTEM_PROMPT,
    temperature=0.1,
)

# Optional: expose for direct import
__all__ = ["root_agent"]