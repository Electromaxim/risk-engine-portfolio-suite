import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.stattools import adfuller
from arch import arch_model
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class ResidualForensics:
    def __init__(self, window: int = 100, anomaly_contamination: float = 0.05):
        self.window = window
        self.contamination = anomaly_contamination
        
    def analyze(self, residuals: pd.Series) -> dict:
        """Comprehensive residual diagnostics"""
        return {
            "stationary": self._check_stationarity(residuals),
            "anomalies": self._detect_anomalies(residuals),
            "volatility_clustering": self._check_volatility_clustering(residuals),
            "autocorrelation": self._calculate_autocorrelation(residuals)
        }
    
    def _check_stationarity(self, series: pd.Series) -> bool:
        """Augmented Dickey-Fuller test"""
        result = adfuller(series.dropna())
        return result[1] < 0.05  # p-value < 5%
    
    def _detect_anomalies(self, residuals: pd.Series) -> pd.Series:
        """Isolation Forest anomaly detection"""
        clf = IsolationForest(
            contamination=self.contamination, 
            random_state=42,
            n_estimators=200
        )
        X = residuals.values.reshape(-1, 1)
        anomalies = clf.fit_predict(X)
        return pd.Series(anomalies == -1, index=residuals.index)
    
    def _check_volatility_clustering(self, series: pd.Series) -> float:
        """Compute volatility persistence (GARCH-like)"""
        squared_returns = series ** 2
        return squared_returns.autocorr(lag=1)
    
    def _calculate_autocorrelation(self, series: pd.Series, lags: list = [1, 5, 10]) -> dict:
        return {f"lag_{lag}": series.autocorr(lag=lag) for lag in lags}
        
        
class ResidualAnalyzer:
    def __init__(self, window: int = 100, alpha: float = 0.05):
        """
        :param window: Rolling window for volatility calculations
        :param alpha: Significance level for statistical tests
        """
        self.window = window
        self.alpha = alpha
        
    def full_analysis(self, residuals: pd.Series) -> dict:
        """Comprehensive residual diagnostics pipeline"""
        return {
            "stationarity": self._test_stationarity(residuals),
            "anomalies": self._detect_anomalies(residuals),
            "volatility_clustering": self._measure_vol_clustering(residuals),
            "autocorrelation": self._calculate_autocorrelations(residuals),
            "garch_fit": self._fit_garch_model(residuals)
        }
    
    def _test_stationarity(self, series: pd.Series) -> dict:
        """Check if residuals are stationary using Augmented Dickey-Fuller test"""
        result = adfuller(series.dropna())
        return {
            "p_value": result[1],
            "stationary": result[1] < self.alpha,
            "test_statistic": result[0]
        }
    
    def _detect_anomalies(self, residuals: pd.Series) -> dict:
        """Identify statistical anomalies using isolation forest"""
        clf = IsolationForest(
            contamination=0.05, 
            random_state=42,
            n_estimators=200
        )
        X = residuals.values.reshape(-1, 1)
        anomalies = clf.fit_predict(X)
        anomaly_dates = residuals.index[anomalies == -1]
        return {
            "count": len(anomaly_dates),
            "dates": anomaly_dates.tolist(),
            "scores": clf.decision_function(X).tolist()
        }
    
    def _measure_vol_clustering(self, series: pd.Series) -> float:
        """Quantify volatility persistence (GARCH effect)"""
        squared = series ** 2
        return squared.rolling(self.window).mean().autocorr(lag=1)
    
    def _calculate_autocorrelations(self, series: pd.Series, lags=(1, 5, 10, 20)) -> dict:
        """Compute autocorrelation at key lags"""
        return {f"lag_{lag}": series.autocorr(lag=lag) for lag in lags}
    
    def _fit_garch_model(self, series: pd.Series) -> dict:
        """Fit GARCH(1,1) model to quantify volatility dynamics"""
        try:
            model = arch_model(series, vol='Garch', p=1, q=1)
            result = model.fit(disp='off')
            return {
                "omega": result.params['omega'],
                "alpha": result.params['alpha[1]'],
                "beta": result.params['beta[1]'],
                "persistence": result.params['alpha[1]'] + result.params['beta[1]']
            }
        except Exception as e:
            logger.error(f"GARCH fitting failed: {e}")
            return {"error": str(e)}
