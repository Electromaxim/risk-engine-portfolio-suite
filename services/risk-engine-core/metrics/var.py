import numpy as np
from simulation.monte_carlo import generate_paths
from models.heston import heston_model
from joblib import Parallel, delayed

def calculate_var(portfolio: dict, confidence: float = 0.95, n_sim: int = 10000) -> float:
    """
    Compute Value-at-Risk using Monte Carlo simulation
    Returns: VaR at specified confidence level
    """
    # Get market parameters from portfolio
    positions = portfolio["positions"]
    T = 1  # 1-day horizon
    
    # Parallel path generation
    results = Parallel(n_jobs=-1)(
        delayed(simulate_portfolio)(positions, T) 
        for _ in range(n_sim)
    )
    
    pnl_changes = np.array(results)
    return np.percentile(pnl_changes, (1 - confidence) * 100)

def simulate_portfolio(positions: list, T: float) -> float:
    """Simulate portfolio value change for one path"""
    pnl = 0.0
    for pos in positions:
        # Generate asset path using Heston model
        S0 = get_current_price(pos["asset_id"])
        _, paths = heston_model(S0, ...)  # Parameters from calibration
        pnl += pos["quantity"] * (paths[-1] - S0)
    return pnl