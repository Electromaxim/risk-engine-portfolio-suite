# services/compliance-security/sgx/gramine_verifier.py
import gramine
from ctypes import c_float

class SGXExposureVerifier:
    def __init__(self):
        self.enclave = gramine.Enclave("enclave_provider/enclave.signed.so")
        
    def verify(self, portfolio: dict, max_exposure: float) -> bool:
        # Convert to C-compatible types
        c_portfolio = (c_float * 4)(*portfolio["asset_values"])
        
        # Execute in enclave
        result = self.enclave.call(
            b"verify_exposure",
            c_portfolio,
            c_float(portfolio["total_value"]),
            c_float(max_exposure)
        )
        return bool(result)