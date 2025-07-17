"""
Action Execution Engine
Converts AI recommendations into trading/risk operations
"""
from portfolio_service.api.client import PortfolioClient
from hedging_simulator import HedgingEngine
import threading
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class ActionExecutor:
    def __init__(self):
        self.portfolio_client = PortfolioClient()
        self.hedger = HedgingEngine()
        self.lock = threading.Lock()
        
    def execute_actions(self, actions: list) -> dict:
        """Execute AI-recommended actions with safety checks"""
        results = {}
        for action in actions:
            try:
                with self.lock:
                    if action["type"] == "rebalance":
                        results[action["type"]] = self._rebalance_portfolio(
                            action["portfolio"], 
                            action["intensity"]
                        )
                    elif action["type"] == "hedge":
                        results[action["type"]] = self._apply_hedge(
                            action["instrument"],
                            action["notional"]
                        )
            except Exception as e:
                logger.error(f"Action execution failed: {e}")
                results[action["type"]] = {"status": "error", "reason": str(e)}
        return results
    
    def _rebalance_portfolio(self, portfolio_id: int, intensity: float) -> dict:
        """Rebalance portfolio based on AI recommendation"""
        # Get current portfolio
        portfolio = self.portfolio_client.get_portfolio(portfolio_id)
        
        # Generate rebalanced version
        rebalanced = self._calculate_rebalance(portfolio, intensity)
        
        # Execute through order management system
        return self.portfolio_client.update_portfolio(rebalanced)
    
    def _calculate_rebalance(self, portfolio: dict, intensity: float) -> dict:
        """Reduce concentrated positions by intensity factor"""
        rebalanced = portfolio.copy()
        for position in rebalanced["positions"]:
            if position["weight"] > 0.1:  # Over 10% allocation
                reduction = position["weight"] * intensity
                position["quantity"] *= (1 - reduction)
        return rebalanced
    
    def _apply_hedge(self, instrument: str, notional: float) -> dict:
        """Execute hedging strategy"""
        return self.hedger.execute_hedge(
            instrument=instrument,
            notional=notional,
            strategy="delta_neutral"
        )