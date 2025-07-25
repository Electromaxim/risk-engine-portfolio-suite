# services/compliance-security/sgx/gramine_verifier.py
import gramine
from azure.attestation import AttestationClient

class SGXExposureVerifier:
    def __init__(self):
        self.enclave = gramine.Enclave("enclave_provider/enclave.signed.so")
        self.attestation_client = AttestationClient(
            endpoint=config.SGX_ATTESTATION_URL,
            credential=DefaultAzureCredential()
        )
    
    def verify(self, portfolio: dict, max_exposure: float) -> bool:
        # Remote attestation first
        self._verify_attestation()
        if not self._verify_attestation():
            return False
        
        # ... existing verification logic ...
    
    def _verify_attestation(self) -> bool:
        """Perform remote attestation via Azure"""
        attestation = self.enclave.get_attestation_evidence()
        result = self.attestation_client.attest_sgx_enclave(attestation)
        return result.is_verified