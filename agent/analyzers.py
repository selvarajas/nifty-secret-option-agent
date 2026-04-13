def analyze_vix(vix: float) -> dict:
    if vix <= 14:
        return {"regime": "Low", "bias": "Option Buying (cheap)", "setup_match": [1]}
    elif 15 <= vix <= 18:
        return {"regime": "Normal", "bias": "Directional", "setup_match": [3]}
    elif 19 <= vix <= 25:
        return {"regime": "Rising", "bias": "Option Selling", "setup_match": [2]}
    else:
        return {"regime": "Panic", "bias": "Mean Reversion", "setup_match": [2, 4]}

def analyze_pcr(option_data: dict) -> float:
    total_ce_oi = sum(item["CE"]["openInterest"] for item in option_data if "CE" in item)
    total_pe_oi = sum(item["PE"]["openInterest"] for item in option_data if "PE" in item)
    return round(total_pe_oi / total_ce_oi, 2) if total_ce_oi else 1.0