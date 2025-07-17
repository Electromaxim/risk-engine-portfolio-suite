class AdaptiveAnonymizer:  
    LIQUIDITY_PROFILES = {  
        "large_cap": {"epsilon": 0.05, "sensitivity": 1e6},  
        "small_cap": {"epsilon": 0.1, "sensitivity": 5e5},  
        "corporate_bond": {"epsilon": 0.2, "sensitivity": 2e5},  
        "derivative": {"epsilon": 0.01, "sensitivity": 1e7}  
    }  

    def anonymize(self, positions: dict, liquidity_tags: dict) -> dict:  
        return {  
            asset: value + Laplace(  
                epsilon=self.LIQUIDITY_PROFILES[liquidity_tags[asset]]["epsilon"],  
                sensitivity=self.LIQUIDITY_PROFILES[liquidity_tags[asset]]["sensitivity"]  
            ).randomise(0)  
            for asset, value in positions.items()  
        }  