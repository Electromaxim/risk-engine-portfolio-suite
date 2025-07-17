from .zokrates_wrapper import ZoKratesProver

class ExposureVerifier:
    def __init__(self):
        self.prover = ZoKratesProver()
        self.circuit = "finma_exposure"
    
    def verify_portfolio_exposure(self, portfolio: dict, max_exposure: float) -> bool:
        # Prepare circuit inputs
        inputs = self._portfolio_to_zok_inputs(portfolio, max_exposure)
        
        # Generate proof
        proof = self.prover.generate_proof(self.circuit, inputs)
        
        # Verify proof
        return self.prover.verify_proof(self.circuit, proof)
    
    def _portfolio_to_zok_inputs(self, portfolio: dict, max_exposure: float) -> list:
        """Map portfolio to ZoKrates circuit inputs"""
        return [
            portfolio["equity_value"],
            portfolio["bond_value"],
            portfolio["derivatives_value"],
            portfolio["cash_value"],
            portfolio["total_value"],
            max_exposure,
            portfolio["client_risk_tier"],
            portfolio["max_liquidity_risk"]
        ]