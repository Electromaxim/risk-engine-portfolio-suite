from simulation.monte_carlo import MonteCarloSimulator
from metrics.var import calculate_var
from metrics.tail_risk import TailRiskCalculator

class FullRiskWorkflow:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.simulator = MonteCarloSimulator(n_simulations=50000)
        self.tail_calculator = TailRiskCalculator()
    
    def calculate_full_risk(self):
        # 1. Simulate portfolio paths
        sim_paths = self._simulate_portfolio()
        
        # 2. Compute P&L distribution
        final_values = sim_paths[:, -1]
        initial_value = self.portfolio.current_value
        pnl = (final_values - initial_value) / initial_value
        
        # 3. Calculate risk metrics
        return {
            "var_99": calculate_var(pnl, confidence=0.99),
            "es_99": self.tail_calculator.expected_shortfall(pnl),
            "tail_loss": self.tail_calculator.tail_loss(pnl),
            "spectral_risk": self.tail_calculator.spectral_risk(pnl)
        }
    
    def _simulate_portfolio(self) -> np.ndarray:
        """Aggregate simulations across assets"""
        portfolio_paths = np.zeros((self.simulator.n_simulations, 
                                   self.simulator.time_steps + 1))
        
        for asset in self.portfolio.assets:
            # Get model parameters from calibration
            params = self._get_asset_params(asset)
            asset_paths = self.simulator.simulate(
                model=asset.risk_model,
                **params
            )
            portfolio_paths += asset_paths * asset.weight
            
        return portfolio_paths