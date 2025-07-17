import numpy as np
import pandas as pd
from metrics.model_performance import ModelValidator

class BreachAnalyzer:
    def __init__(self, confidence: float = 0.99):
        self.confidence = confidence
        self.validator = ModelValidator()

    def analyze_breaches(self, pnl_series: pd.Series, var_series: pd.Series) -> dict:
        """Compute key backtesting metrics"""
        breaches = pnl_series < -var_series
        breach_dates = pnl_series[breaches].index
        
        # Kupiec POF test
        pof_pvalue = self.validator.binomial_test(
            breaches.sum(), 
            len(pnl_series), 
            self.confidence
        )
        
        # Christoffersen independence test
        independence_pvalue = self.validator.conditional_coverage(breaches.astype(int).values)
        
        return {
            "breach_count": int(breaches.sum()),
            "breach_dates": breach_dates.tolist(),
            "coverage_ratio": 1 - (breaches.sum() / len(pnl_series)),
            "pof_pvalue": pof_pvalue,
            "independence_pvalue": independence_pvalue,
            "traffic_light": self._traffic_light(breaches.sum())
        }
    
    def _traffic_light(self, breach_count: int) -> str:
        """Basel traffic light system"""
        if breach_count <= 4: return "GREEN"
        if breach_count <= 9: return "AMBER"
        return "RED"