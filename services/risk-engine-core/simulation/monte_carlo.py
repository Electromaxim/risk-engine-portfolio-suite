"""
Advanced Monte Carlo Framework
Flexible path simulation for multiple asset classes
"""
import numpy as np
from models.heston import heston_paths
from models.jump_diffusion import jump_diffusion_paths
from lib_utils.parallel import parallelize

class MonteCarloSimulator:
    def __init__(self, n_simulations=10000, time_steps=252, seed=42):
        self.n_simulations = n_simulations
        self.time_steps = time_steps
        self.seed = seed
        np.random.seed(seed)
    
    def simulate(self, model: str, **params) -> np.ndarray:
        """
        Unified simulation interface
        Supported models: 'heston', 'jump_diffusion', 'black_scholes'
        """
        if model == 'heston':
            return self._simulate_heston(**params)
        elif model == 'jump_diffusion':
            return self._simulate_jump_diffusion(**params)
        elif model == 'black_scholes':
            return self._simulate_bs(**params)
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    @parallelize
    def _simulate_heston(self, S0, v0, r, kappa, theta, sigma, rho) -> np.ndarray:
        """Parallelized Heston simulation"""
        return heston_paths(
            S0, v0, r, kappa, theta, sigma, rho,
            T=1.0, N=self.time_steps, n_paths=self.n_simulations
        )
    
    @parallelize
    def _simulate_jump_diffusion(self, S0, r, sigma, jump_lambda, jump_mu, jump_sigma) -> np.ndarray:
        """Merton's jump diffusion model"""
        return jump_diffusion_paths(
            S0, r, sigma, jump_lambda, jump_mu, jump_sigma,
            T=1.0, n_steps=self.time_steps, n_paths=self.n_simulations
        )
    
    def _simulate_bs(self, S0, r, sigma) -> np.ndarray:
        """Black-Scholes geometric Brownian motion"""
        dt = 1.0 / self.time_steps
        paths = np.zeros((self.n_simulations, self.time_steps + 1))
        paths[:, 0] = S0
        
        for t in range(1, self.time_steps + 1):
            z = np.random.standard_normal(self.n_simulations)
            paths[:, t] = paths[:, t-1] * np.exp(
                (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
            )
        return paths