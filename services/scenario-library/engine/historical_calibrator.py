class HistoricalCalibrator:
    def calibrate_to_event(self, event_name: str, portfolio: dict) -> dict:
        """
        Adjust historical scenario to portfolio's current composition
        :param event_name: "gfc_2008", "covid_crash", etc.
        :return: Calibrated shock parameters
        """
        base_scenario = self.scenario_store.get(event_name)
        
        # Adjust shocks based on portfolio beta
        calibrated = {}
        for asset_class, shock in base_scenario["parameters"].items():
            beta = self._calculate_portfolio_beta(portfolio, asset_class)
            calibrated[asset_class] = shock * beta
            
        return {
            "base_scenario": event_name,
            "calibrated_parameters": calibrated,
            "calibration_date": datetime.utcnow()
        }
    
    def _calculate_portfolio_beta(self, portfolio: dict, asset_class: str) -> float:
        """Compute sensitivity to historical shocks"""
        # Implementation using portfolio's asset correlations
        return 1.2  # Placeholder