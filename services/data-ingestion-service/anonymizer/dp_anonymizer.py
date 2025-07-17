import numpy as np
from diffprivlib.mechanisms import Laplace

class DPAnonymizer:
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon
    
    def anonymize_positions(self, positions: dict) -> dict:
        """Add Laplace noise to position sizes"""
        mech = Laplace(epsilon=self.epsilon, sensitivity=1e6)
        anonymized = {}
        for asset, value in positions.items():
            anonymized[asset] = value + mech.randomise(0)
        return anonymized
    
    def tokenize_client_ids(self, client_ids: list) -> dict:
        """Replace client IDs with SHA-256 hashes"""
        import hashlib
        return {cid: hashlib.sha256(cid.encode()).hexdigest() for cid in client_ids}