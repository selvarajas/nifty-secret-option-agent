from .analyzers import analyze_vix, analyze_pcr

class StrategyEngine:
    @staticmethod
    def recommend(vix: float, pcr: float, oi_shift: str, vp: dict, price_action: str):
        vix_analysis = analyze_vix(vix)
        regime = vix_analysis["regime"]

        # Setup 1: Low VIX Breakout
        if regime == "Low" and 11 <= vix <= 13 and "tight_balance" in price_action:
            return {
                "setup": "COMPLETE STRATEGY SETUP 1: LOW VIX BREAKOUT TRADE",
                "action": "BUY ATM Options",
                "logic": "Low VIX = market sleeping → breakout gives explosive move",
                "target": "LVN expansion move",
                "confidence": "HIGH"
            }

        # Setup 2: High VIX Mean Reversion
        if vix >= 22:
            return {
                "setup": "COMPLETE STRATEGY SETUP 2: HIGH VIX MEAN REVERSION",
                "action": "SELL Options (Iron Condor / Credit Spread)",
                "logic": "High VIX = panic already priced → market cools down",
                "confidence": "HIGH"
            }

        # Setup 3: Trend Continuation (Best Setup)
        if regime == "Normal" and pcr > 1.2 and "put_writing_increasing" in oi_shift:
            return {
                "setup": "COMPLETE STRATEGY SETUP 3: TREND CONTINUATION (BEST SETUP)",
                "action": "Buy on dip (CE or Futures)",
                "logic": "Smart money accumulating → controlled trend",
                "confidence": "VERY HIGH"
            }

        # Setup 4: Reversal Warning
        if "nifty_rising_but_vix_rising" in oi_shift:
            return {
                "setup": "COMPLETE STRATEGY SETUP 4: REVERSAL WARNING (ADVANCED)",
                "action": "Prepare for SHORT",
                "logic": "Hidden fear building → distribution phase",
                "confidence": "MEDIUM"
            }

        return {"setup": "NO CLEAR SETUP", "action": "Wait / Monitor", "logic": "Conditions not aligned", "confidence": "LOW"}