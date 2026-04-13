from google.adk import Orchestrator

from fastapi import FastAPI

from .vix_agent import vix_agent
from .strategy_agent import strategy_agent
from .tools import fetch_india_vix, fetch_nifty_option_chain, fetch_nifty_volume_profile
from .analyzers import analyze_pcr

orchestrator = Orchestrator(
    name="NiftySecretOptionOrchestrator",
    agents=[vix_agent, strategy_agent],
    model="gemini-2.0-flash-exp"
)

app = FastAPI(title="Nifty Secret Option Agent v2.0 - Multi-Agent")

@app.get("/recommend")
async def recommend_trade():
    vix_data = await fetch_india_vix()
    chain = await fetch_nifty_option_chain()
    vp = await fetch_nifty_volume_profile()
    pcr = analyze_pcr(chain)

    # Multi-agent flow
    vix_result = await vix_agent.run(f"Current VIX: {vix_data['vix']}")
    strategy_result = await strategy_agent.run(
        f"VIX Regime: {vix_result}\nPCR: {pcr}\nVolume Profile: {vp}\nDecide Setup 1-4"
    )

    return {
        "vix_agent_output": vix_result,
        "strategy_agent_output": strategy_result,
        "final_recommendation": strategy_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)