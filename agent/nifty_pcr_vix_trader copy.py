import requests
import json
from datetime import datetime
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

# ====================== CUSTOM TOOL ======================
def fetch_nifty_market_data() -> str:
    """Fetches live Nifty option chain + INDIA VIX and computes PCR (OI & Volume)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 1. Option Chain (NIFTY)
    oc_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    oc_resp = requests.get(oc_url, headers=headers)
    oc_data = oc_resp.json()
    
    # Nearest expiry
    expiry = oc_data["records"]["expiryDates"][0]
    records = [r for r in oc_data["records"]["data"] if r["expiryDate"] == expiry]
    
    call_oi = sum(r["CE"]["openInterest"] for r in records if "CE" in r)
    put_oi = sum(r["PE"]["openInterest"] for r in records if "PE" in r)
    call_vol = sum(r["CE"]["totalTradedVolume"] for r in records if "CE" in r)
    put_vol = sum(r["PE"]["totalTradedVolume"] for r in records if "PE" in r)
    
    pcr_oi = round(put_oi / call_oi, 4) if call_oi else 0
    pcr_vol = round(put_vol / call_vol, 4) if call_vol else 0
    
    # 2. INDIA VIX
    vix_url = "https://www.nseindia.com/api/historicalOR/vixhistory?from=01-04-2026&to=19-04-2026
"
    vix_resp = requests.get(vix_url, headers=headers)
    vix_data = vix_resp.json()["data"][0]
    vix_value = round(vix_data["lastPrice"], 2)
    
    nifty_spot = round(oc_data["records"]["underlyingValue"], 2)
    
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nifty_spot": nifty_spot,
        "india_vix": vix_value,
        "pcr_oi": pcr_oi,
        "pcr_volume": pcr_vol,
        "nearest_expiry": expiry,
        "call_oi_total": call_oi,
        "put_oi_total": put_oi,
        "call_vol_total": call_vol,
        "put_vol_total": put_vol
    }
    return json.dumps(result, indent=2)

# ====================== SUB-AGENTS ======================
GEMINI_MODEL = "gemini-2.5-flash"   # or gemini-2.5-pro if you have access

data_fetcher = LlmAgent(
    name="DataFetcherAgent",
    model=GEMINI_MODEL,
    instruction="You are a market data specialist. Call the fetch_nifty_market_data tool and return ONLY the raw JSON result.",
    tools=[fetch_nifty_market_data],
    output_key="market_data_json"
)

analyzer = LlmAgent(
    name="AnalyzerAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are an expert Nifty options analyst.
    Market data: {market_data_json}
    
    Rules (use both PCRs + VIX):
    - PCR_OI > 1.30 AND VIX > 18   → Strong contrarian BULLISH (buy calls)
    - PCR_OI < 0.80 AND VIX > 18   → Strong contrarian BEARISH (buy puts)
    - PCR_Volume > 1.40            → Intraday bearish momentum
    - PCR_Volume < 0.70            → Intraday bullish momentum
    - Neutral zone: 0.85-1.15
    
    Output JSON only:
    {{"signal": "BULLISH"|"BEARISH"|"NEUTRAL", "confidence": 0-100, "reason": "short explanation"}}
    """,
    output_key="signal_json"
)

strategist = LlmAgent(
    name="StrategistAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a Nifty options strategist.
    Market data: {market_data_json}
    Signal: {signal_json}
    
    Generate a precise trade:
    - Recommended strike (ATM ± 100-200 based on signal)
    - CE or PE
    - Lot size suggestion (1-3 lots max)
    - Target & Stop-loss (%)
    - Expected holding time (expiry day or intraday)
    
    Output ONLY valid JSON:
    {{"action": "BUY_CE"|"BUY_PE"|"HOLD", "strike": number, "lots": number, "target": number, "stop_loss": number, "rationale": "brief"}}
    """,
    output_key="trade_plan_json"
)

executor = LlmAgent(
    name="TradeExecutorAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are the final executor.
    Trade plan: {trade_plan_json}
    
    If action is BUY_CE or BUY_PE → print "EXECUTING TRADE: ..." (or call real broker API).
    Otherwise say "NO TRADE".
    
    For simulation: just print the order.
    For real trading: replace the print with your broker code (Kite / Upstox etc.).
    """,
    output_key="execution_result"
)

# ====================== ORCHESTRATOR ======================
nifty_trading_agent = SequentialAgent(
    name="NiftyPCRVIXTrader",
    sub_agents=[data_fetcher, analyzer, strategist, executor],
    description="Full PCR (Volume+OI) + VIX powered Nifty options trading agent"
)

# ====================== RUN ======================
if __name__ == "__main__":
    print("🚀 Starting Nifty PCR + VIX Trading Agent (Google ADK)...\n")
    result=fetch_nifty_market_data()
   #result = nifty_trading_agent.run("Analyze Nifty options right now and execute if signal is strong.")
    print("\n=== FINAL OUTPUT ===")
    
    print(result)