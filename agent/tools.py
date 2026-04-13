import httpx
import pandas as pd
from .config import NSE_HEADERS

async def fetch_india_vix() -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://www.nseindia.com/api/allIndices", headers=NSE_HEADERS)
        data = resp.json()["indices"]
        vix = next((i for i in data if i["index"] == "INDIA VIX"), None)
        return {"vix": round(vix["last"], 2), "change": vix["percentChange"]} if vix else {"vix": 0, "change": 0}

async def fetch_nifty_option_chain() -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY",
            headers=NSE_HEADERS
        )
        return resp.json()["records"]["data"]

async def fetch_nifty_volume_profile() -> dict:
    """Simplified Volume Profile (last 5 days 5-min data + HVN/LVN calc)"""
    # In production replace with full OHLCV + proper VP calculation
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://www.nseindia.com/api/equity-stock?symbol=NIFTY", headers=NSE_HEADERS)
        # Mock realistic levels for demo (real implementation uses pandas volume bins)
        return {
            "hv_n": 24500,
            "lv_n": 24200,
            "vah": 24650,
            "val": 24350,
            "vpoc": 24500
        }