class RiskAlertManager:
    HIGH_RISK_THRESHOLDS = {
        "var_99": 10_000_000,  # CHF
        "es_99": 15_000_000,
        "liquidity_risk": 0.3
    }
    
    def check_breaches(self, metrics):
        for metric, threshold in self.HIGH_RISK_THRESHOLDS.items():
            if metrics.get(metric, 0) > threshold:
                self.trigger_alert(f"{metric} breach: {metrics[metric]} > {threshold}")