from zokrates import zokrates
import hashlib

class ExposureVerifier:
    def __init__(self, circuit_path: str = "zk/circuits/exposure_check.zok"):
        self.circuit = zokrates.compile_from(circuit_path)
        self.setup = zokrates.setup(self.circuit)

    def generate_proof(self, portfolio_hash: str, max_exposure: float) -> dict:
        """Generate ZK proof that exposure < threshold without revealing values"""
        witness = zokrates.compute_witness(
            self.circuit, 
            [portfolio_hash, max_exposure]
        )
        proof = zokrates.generate_proof(self.circuit, witness, self.setup["proving_key"])
        return {
            "proof": proof,
            "verification_key": self.setup["verification_key"]
        }

    @staticmethod
    def hash_portfolio(portfolio: dict) -> str:
        """Create deterministic portfolio hash"""
        serialized = json.dumps(portfolio, sort_keys=True).encode()
        return hashlib.sha256(serialized).hexdigest()

# Corresponding ZoKrates circuit (zk/circuits/exposure_check.zok)
"""
import "hashes/sha256/512bitPadded" as sha256;

def main(private field portfolio_value, field max_exposure) -> bool:
    // Constraint: portfolio_value <= max_exposure
    field exposure_ok = if portfolio_value <= max_exposure then 1 else 0 fi;
    
    // Ensure exposure constraint is satisfied
    assert(exposure_ok == 1);
    return true;
}
"""