class AdaptiveAnonymizer:  
    ASSET_EPSILON = {  
        "equity": 0.05,  
        "corporate_bond": 0.1,  
        "government_bond": 0.3,  
        "derivative": 0.02  
    }  

    def anonymize_positions(self, positions: dict, asset_classes: dict) -> dict:  
        anonymized = {}  
        for asset, value in positions.items():  
            epsilon = self.ASSET_EPSILON.get(  
                asset_classes.get(asset, "equity"),  
                0.1  # Default  
            )  
            mech = Laplace(epsilon=epsilon, sensitivity=1e6)  
            anonymized[asset] = value + mech.randomise(0)  
        return anonymized  