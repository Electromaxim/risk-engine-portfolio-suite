from drift_alert import DriftAlertSystem
from lib_utils.config import get_config

config = get_config()

class BacktestAlerter:
    def __init__(self):
        self.drift_alerter = DriftAlertSystem(threshold=0.3)
    
    def check_backtest_results(self, results: dict):
        """Trigger alerts for concerning backtest outcomes"""
        # Alert on traffic light status
        if results["green_amber_red"] != "GREEN":
            self._trigger_regulatory_alert(results)
        
        # Alert on coverage ratio
        if results["coverage_ratio"] < 0.975:  # <97.5% coverage
            self._trigger_coverage_alert(results)
        
        # Check distribution drift
        hist_pnl = self._load_historical_pnl()
        sim_pnl = self._load_simulated_pnl()
        drift_metric = ModelValidator.distribution_drift(hist_pnl, sim_pnl)
        self.drift_alerter.check_and_alert(hist_pnl, sim_pnl)

    def _trigger_regulatory_alert(self, results: dict):
        # Implementation would use Slack/Email integration
        print(f"🚨 REGULATORY ALERT: {results['green_amber_red']} zone - {results['exceptions_count']} breaches")

    def _trigger_coverage_alert(self, results: dict):
        print(f"⚠️ COVERAGE ALERT: {results['coverage_ratio']:.2%} < 97.5% threshold")