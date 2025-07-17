class AdaptiveAnonymizer:
    ASSET_PROFILES = {
        "large_cap_equity": {"epsilon": 0.05, "sensitivity": 1e6},
        "small_cap_equity": {"epsilon": 0.1, "sensitivity": 5e5},
        "government_bond": {"epsilon": 0.3, "sensitivity": 2e5},
        "corporate_bond": {"epsilon": 0.2, "sensitivity": 3e5},
        "fx_derivative": {"epsilon": 0.01, "sensitivity": 2e6}
    }
    
    def anonymize_position(self, asset_id: str, value: float) -> float:
        profile = self._get_asset_profile(asset_id)
        mech = Laplace(epsilon=profile["epsilon"], sensitivity=profile["sensitivity"])
        return value + mech.randomise(0)
    
    def _get_asset_profile(self, asset_id: str) -> dict:
        """Get anonymization profile from security master"""
        asset_type = self.security_master.get_asset_type(asset_id)
        return self.ASSET_PROFILES.get(asset_type, {"epsilon": 0.1, "sensitivity": 1e6})