import numpy as np
from services.risk-engine-core.models.heston_gpu import simulate_heston_gpu

class ProductionDeltaHedger:
    def __init__(self, portfolio, risk_free_rate: float = 0.01, transaction_cost: float = 0.0001):
        self.portfolio = portfolio
        self.r = risk_free_rate
        self.transaction_cost = transaction_cost  # 1bp transaction cost

    def hedge_portfolio(self, S0: float, T: float, params: dict, n_steps: int = 30) -> dict:
        """Full production hedging with Heston simulation and transaction costs"""
        dt = T / n_steps
        kappa, theta, sigma, rho, v0 = params['kappa'], params['theta'], params['sigma'], params['rho'], params['v0']
        
        # Initialize tracking
        hedge_costs = 0.0
        shares_held = 0
        cash = 0
        current_delta = self._compute_delta(S0, T, v0, params)
        
        # Buy initial hedge
        shares_held = current_delta
        cash = -current_delta * S0
        hedge_costs += abs(current_delta) * S0 * self.transaction_cost
        
        for i in range(1, n_steps+1):
            t = T - i * dt
            
            # Simulate next price with Heston
            paths, vols = simulate_heston_gpu(
                S0=S0, v0=v0, r=self.r,
                kappa=kappa, theta=theta,
                sigma=sigma, rho=rho,
                T=dt, N=5, n_paths=1
            )
            S = paths[0][-1]
            v0 = vols[0][-1]  # Update volatility state
            
            new_delta = self._compute_delta(S, t, v0, params)
            delta_change = new_delta - shares_held
            
            # Rebalance with transaction costs
            cash -= delta_change * S
            hedge_costs += abs(delta_change) * S * self.transaction_cost
            shares_held = new_delta
            S0 = S
        
        # Close positions at expiration
        cash += shares_held * S
        hedge_costs += abs(shares_held) * S * self.transaction_cost
        
        return {
            "final_cash": cash,
            "hedging_cost": hedge_costs,
            "net_pnl": cash - hedge_costs
        }
    
    def _compute_delta(self, S: float, t: float, v: float, params: dict) -> float:
        """Delta calculation using calibrated parameters"""
        # Implementation same as before