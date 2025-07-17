from models.jump_diffusion import jump_diffusion_paths
from scipy.optimize import minimize

class JumpModelCalibrator:
    def calibrate(self, prices: np.ndarray) -> dict:
        """Calibrate jump diffusion to historical returns"""
        returns = np.diff(np.log(prices))
        init_params = [0.1, -0.05, 0.15, 0.05]  # σ, λ, μ_j, σ_j
        
        result = minimize(
            self._mse_to_historical,
            init_params,
            args=(returns),
            bounds=[
                (0.01, 0.5),    # σ
                (0.001, 0.2),   # λ (jump freq)
                (-0.2, 0),      # μ_j (mean jump)
                (0.01, 0.3)     # σ_j (jump vol)
            ]
        )
        return {
            "sigma": result.x[0],
            "jump_lambda": result.x[1],
            "jump_mu": result.x[2],
            "jump_sigma": result.x[3]
        }
    
    def _mse_to_historical(self, params, historical_returns):
        """Compare simulated vs historical distribution"""
        # Simulate returns with current params
        sim_returns = self._simulate_returns(
            sigma=params[0],
            jump_lambda=params[1],
            jump_mu=params[2],
            jump_sigma=params[3],
            n=len(historical_returns)
        )
        
        # Compare distribution statistics
        stats = [
            np.mean(historical_returns),
            np.std(historical_returns),
            np.skew(historical_returns),
            np.kurtosis(historical_returns)
        ]
        sim_stats = [
            np.mean(sim_returns),
            np.std(sim_returns),
            np.skew(sim_returns),
            np.kurtosis(sim_returns)
        ]
        
        return np.sum((np.array(stats) - np.array(sim_stats))**2)