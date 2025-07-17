import numpy as np
from models.black_scholes import black_scholes_delta

class DeltaHedger:
    def __init__(self, portfolio, risk_free_rate: float = 0.01):
        self.portfolio = portfolio
        self.r = risk_free_rate

    def compute_delta(self, S: float, t: float, sigma: float) -> float:
        """Compute total delta exposure of portfolio"""
        total_delta = 0.0
        for position in self.portfolio:
            if position["type"] == "option":
                delta = black_scholes_delta(
                    S, position["strike"], t, self.r, sigma, position["option_type"]
                )
                total_delta += position["quantity"] * delta
            elif position["type"] == "stock":
                total_delta += position["quantity"]
        return total_delta

    def hedge_portfolio(self, S0: float, T: float, sigma: float, n_steps: int = 30) -> dict:
        """Simulate delta hedging over option lifetime"""
        dt = T / n_steps
        hedge_costs = 0.0
        current_delta = self.compute_delta(S0, T, sigma)
        shares_held = current_delta
        cash = -current_delta * S0  # Borrow to buy shares
        
        for i in range(1, n_steps+1):
            t = T - i * dt
            S = self._simulate_price(S0, sigma, dt)  # Use Heston model in production
            
            new_delta = self.compute_delta(S, t, sigma)
            delta_change = new_delta - current_delta
            
            # Rebalance portfolio
            cash -= delta_change * S  # Buy/sell shares
            hedge_costs += abs(delta_change) * S * 0.01  # 1% transaction cost
            
            current_delta = new_delta
            S0 = S
        
        # Close positions at expiration
        cash += current_delta * S
        hedge_costs += abs(current_delta) * S * 0.01
        
        return {
            "final_cash": cash,
            "hedging_cost": hedge_costs,
            "net_pnl": cash - hedge_costs
        }
    
    def _simulate_price(self, S0: float, sigma: float, dt: float) -> float:
        """Simplified price simulation (replace with Heston in prod)"""
        """return S0 * np.exp((self.r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.randn())"""
        from models.heston_gpu import simulate_heston_gpu  
        paths, _ = simulate_heston_gpu(  
        S0=S0, v0=self.v0, r=self.r,  
        kappa=self.kappa, theta=self.theta,  
        sigma=self.sigma, rho=self.rho,  
        T=dt, N=5, n_paths=1  
    )  
    return paths[0][-1]  # Return final simulated price