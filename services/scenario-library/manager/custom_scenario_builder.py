class CustomScenarioDesigner:
    def create_scenario(self, parameters: dict) -> str:
        """
        Create custom stress scenario from user inputs
        :param parameters: {
            "equity_shock": -0.25, 
            "fx_shifts": {"EURCHF": -0.15},
            "volatility_spike": 0.40,
            "correlation_breakdown": True
        }
        :return: Scenario ID
        """
        scenario_id = f"CUSTOM_{uuid.uuid4().hex[:8]}"
        self._validate_parameters(parameters)
        
        # Store with metadata
        self.scenario_db.insert({
            "id": scenario_id,
            "type": "custom",
            "parameters": parameters,
            "created_by": current_user,
            "created_at": datetime.utcnow()
        })
        return scenario_id
    
    def _validate_parameters(self, params: dict):
        """Ensure scenario parameters are within safe limits"""
        if params.get("equity_shock", 0) < -0.5:
            raise ValueError("Equity shock exceeds maximum (-50%)")
        if any(abs(v) > 0.25 for v in params.get("fx_shifts", {}).values()):
            raise ValueError("FX shift exceeds ±25% limit")