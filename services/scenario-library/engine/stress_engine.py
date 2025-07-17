"""
Portfolio Stress Testing Engine
Applies historical/custom scenarios to portfolios with risk factor calibration
"""
import numpy as np
from scipy.stats import zscore
from lib_data.fx import FXConverter
from lib_utils.parallel import parallel_apply
from database import get_scenario_db
import logging

logger = logging.getLogger(__name__)

class StressEngine:
    def __init__(self):
        self.fx = FXConverter()
        self.db = get_scenario_db()
        
    def apply_scenario(self, portfolio: dict, scenario_id: str) -> dict:
        """
        Apply shock scenario to portfolio with automatic calibration
        :param portfolio: {
            "positions": [
                {"asset_id": "AAPL US", "qty": 1000, "price": 182.3, "currency": "USD"},
                ...
            ],
            "base_currency": "CHF"
        }
        :param scenario_id: "gfc_2008", "covid_2020", or custom ID
        :return: Shocked portfolio with P&L impact
        """
        scenario = self._load_scenario(scenario_id)
        shocked_portfolio = portfolio.copy()
        total_pnl = 0.0
        
        # Parallel shock application
        results = parallel_apply(
            func=self._apply_asset_shock,
            items=portfolio["positions"],
            scenario=scenario,
            base_ccy=portfolio["base_currency"]
        )
        
        for asset, new_value, pnl in results:
            shocked_portfolio["positions"][asset] = new_value
            total_pnl += pnl
            
        shocked_portfolio["scenario_pnl"] = total_pnl
        shocked_portfolio["scenario_id"] = scenario_id
        return shocked_portfolio

    def _apply_asset_shock(self, position: dict, scenario: dict, base_ccy: str) -> tuple:
        """Apply scenario shocks to individual position"""
        # Get asset-specific shock factor
        shock_factor = self._get_shock_factor(position["asset_class"], scenario)
        
        # Apply price shock
        original_value = position["qty"] * position["price"]
        new_price = position["price"] * (1 + shock_factor)
        new_value = position["qty"] * new_price
        
        # FX conversion if needed
        if position["currency"] != base_ccy:
            fx_rate = self.fx.get_rate(
                f"{position['currency']}{base_ccy}", 
                scenario["as_of_date"]
            )
            new_value *= fx_rate
            original_value *= fx_rate
            
        return (
            position["asset_id"],
            {**position, "price": new_price},
            new_value - original_value
        )

    def _get_shock_factor(self, asset_class: str, scenario: dict) -> float:
        """Get calibrated shock based on asset beta and scenario"""
        base_shock = scenario["parameters"][asset_class]
        beta = self._get_asset_beta(asset_class, scenario["base_scenario"])
        return base_shock * beta
        
    def _get_asset_beta(self, asset_class: str, base_scenario: str) -> float:
        """Compute sensitivity to historical scenario (1.0 = average sensitivity)"""
        # Implementation would use historical covariance matrix
        return 1.15  # Placeholder for 15% higher sensitivity