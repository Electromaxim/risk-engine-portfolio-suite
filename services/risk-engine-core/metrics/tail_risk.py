"""
Advanced Tail Risk Metrics
Beyond VaR for extreme risk quantification
"""
import numpy as np
from scipy.stats import genpareto

class TailRiskCalculator:
    def expected_shortfall(self, losses: np.ndarray, confidence: float = 0.99) -> float:
        """Conditional Value-at-Risk (CVaR)"""
        var = np.quantile(losses, confidence)
        return losses[losses >= var].mean()
    
    def tail_loss(self, losses: np.ndarray, confidence: float = 0.99) -> float:
        """Probability-weighted tail loss"""
        var = np.quantile(losses, confidence)
        tail = losses[losses >= var]
        return np.sum(tail - var) / len(losses)
    
    def extreme_value_es(self, losses: np.ndarray, confidence: float = 0.995) -> float:
        """EVT-based Expected Shortfall for very high confidence"""
        # Fit Generalized Pareto Distribution to tail
        var = np.quantile(losses, 0.95)
        tail = losses[losses > var] - var
        
        # Fit GPD
        params = genpareto.fit(tail)
        xi, beta = params[0], params[2]  # Shape and scale
        
        # EVT ES formula
        u = 1 - confidence
        return var + (beta + xi * var) / (1 - xi)
    
    def spectral_risk(self, losses: np.ndarray, risk_aversion: float = 0.8) -> float:
        """Weighted risk measure sensitive to tail shape"""
        sorted_losses = np.sort(losses)
        weights = self._generate_weights(len(losses), risk_aversion)
        return np.sum(weights * sorted_losses)
    
    def _generate_weights(self, n: int, risk_aversion: float) -> np.ndarray:
        """Exponentially increasing weights for tail losses"""
        k = np.arange(1, n + 1)
        return (risk_aversion - 1) * (1 - risk_aversion)**(k - 1) / risk_aversion