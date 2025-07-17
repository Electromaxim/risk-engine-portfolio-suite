import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class ResidualAnalyzer:
    def __init__(self, window: int = 100):
        self.window = window

    def detect_anomalies(self, residuals: pd.Series) -> pd.Series:
        """Detect model residual anomalies using isolation forest"""
        # Reshape for sklearn
        X = residuals.values.reshape(-1, 1)
        
        # Train anomaly detector
        clf = IsolationForest(contamination=0.05, random_state=42)
        anomalies = clf.fit_predict(X)
        
        return pd.Series(anomalies == -1, index=residuals.index)

    def analyze_residual_patterns(self, residuals: pd.Series) -> dict:
        """Identify systematic biases in model residuals"""
        # Rolling mean and volatility
        mean_bias = residuals.rolling(self.window).mean()
        vol_change = residuals.rolling(self.window).std()
        
        # Autocorrelation analysis
        autocorr = [residuals.autocorr(lag=i) for i in [1, 5, 10]]
        
        return {
            "mean_bias": mean_bias.iloc[-1],
            "volatility_change": vol_change.iloc[-1],
            "autocorrelation": autocorr,
            "stationary": self._is_stationary(residuals)
        }
    
    def _is_stationary(self, series: pd.Series) -> bool:
        """ADF test for stationarity"""
        from statsmodels.tsa.stattools import adfuller
        result = adfuller(series.dropna())
        return result[1] < 0.05  # p-value < 5%