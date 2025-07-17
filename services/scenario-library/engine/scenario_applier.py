import pandas as pd
from presets import GFC_2008, COVID_CRASH
from lib_data.fx import convert_currency
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class ScenarioApplier:
    SCENARIOS = {
        "gfc_2008": GFC_2008,
        "covid_crash": COVID_CRASH
    }

    def apply_scenario(self, portfolio: dict, scenario_id: str, base_currency: str = "CHF") -> dict:
        """Apply historical scenario shocks to portfolio"""
        if scenario_id not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_id}")
        
        scenario = self.SCENARIOS[scenario_id]
        shocked_portfolio = portfolio.copy()
        
        # Apply equity shocks
        for position in shocked_portfolio["positions"]:
            asset_type = position["asset_class"]
            
            # Equity shock
            if asset_type == "equity":
                position["current_price"] *= (1 + scenario["parameters"]["equity_shock"])
            
            # FX adjustment
            if position["currency"] != base_currency:
                fx_pair = f"{position['currency']}{base_currency}"
                if fx_pair in scenario["parameters"]["fx_shifts"]:
                    new_rate = scenario["parameters"]["fx_shifts"][fx_pair]
                    position["current_price"] *= new_rate
                    position["currency"] = base_currency
        
        # Apply interest rate shocks
        if "fixed_income" in shocked_portfolio:
            for bond in shocked_portfolio["fixed_income"]:
                ccy = bond["currency"]
                if ccy in scenario["parameters"]["rates_shifts"]:
                    yield_change = scenario["parameters"]["rates_shifts"][ccy]
                    bond["yield"] += yield_change
                    bond["price"] = self._adjust_bond_price(bond, yield_change)
        
        logger.info(f"Applied {scenario['name']} scenario to portfolio")
        return shocked_portfolio
    
    def _adjust_bond_price(self, bond: dict, yield_delta: float) -> float:
        """Simple bond price adjustment for yield changes"""
        duration = bond.get("duration", 5)  # Default 5y duration
        return bond["price"] * (1 - duration * yield_delta / 100)