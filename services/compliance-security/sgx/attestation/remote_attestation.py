from azure.attestation import AttestationClient
from azure.identity import DefaultAzureCredential

class RemoteAttestor:
    def __init__(self):
        self.client = AttestationClient(
            endpoint=config.SGX_ATTESTATION_URL,
            credential=DefaultAzureCredential()
        )
    
    def verify_attestation(self, evidence: bytes) -> bool:
        """Verify SGX enclave attestation via Intel AS"""
        result = self.client.attest_sgx_enclave(evidence)
        return result.is_verified and \
               result.sgx_mr_enclave == config.EXPECTED_MR_ENCLAVE