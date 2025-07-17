# services/compliance-security/hsm/hsm_verifier.py
from ibm_zseries import CryptoExpress

class HSMVerifier:
    def __init__(self):
        self.hsm = CryptoExpress(
            partition_id=config.HSM_PARTITION,
            key_label="FINMA_VERIFICATION_KEY"
        )
    
    def verify_exposure(self, portfolio_hash: bytes, proof: bytes) -> bool:
        """Offload verification to dedicated hardware"""
        return self.hsm.verify_signature(
            data=portfolio_hash,
            signature=proof,
            algorithm="RSA_PSS_SHA384"
        )