from lib_data.fx import convert_currency

def validate_position_concentrations(positions: list) -> dict:
    """FINMA concentration risk checks (LIMIT: 25% per asset)"""
    total_value = sum(p["notional"] for p in positions)
    alerts = []
    for pos in positions:
        weight = pos["notional"] / total_value
        if weight > 0.25:
            alerts.append(f"Concentration breach: {pos['asset_id']} ({weight:.1%})")
    
    # FX sanity check
    if len(set(p["currency"] for p in positions)) > 15:
        alerts.append("Excessive currency exposure (>15 currencies)")
    
    return {"valid": len(alerts) == 0, "alerts": alerts}