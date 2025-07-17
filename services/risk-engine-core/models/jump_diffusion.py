"""
Merton's Jump Diffusion Model
Captures sudden market moves via Poisson jumps
"""
import numpy as np

def jump_diffusion_paths(S0, r, sigma, jump_lambda, jump_mu, jump_sigma, T=1.0, n_steps=252, n_paths=10000):
    """
    Simulate asset paths with jumps
    :param jump_lambda: Average jumps per year
    :param jump_mu: Mean jump size
    :param jump_sigma: Std dev of jump size
    """
    dt = T / n_steps
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S0
    
    # Jump parameters
    jump_prob = jump_lambda * dt
    
    for t in range(1, n_steps + 1):
        # Standard Brownian motion
        z = np.random.standard_normal(n_paths)
        diffusion = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
        
        # Jump component
        jump_occurred = np.random.poisson(jump_prob, n_paths) > 0
        jump_size = np.zeros(n_paths)
        jump_size[jump_occurred] = np.random.normal(jump_mu, jump_sigma, np.sum(jump_occurred))
        
        # Combine components
        paths[:, t] = paths[:, t-1] * np.exp(diffusion + jump_size)
    
    return paths