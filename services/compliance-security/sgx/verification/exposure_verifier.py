# services/compliance-security/sgx/verification/exposure_verifier.py
import ctypes
from sgx_urts import sgx_enclave_lib
from .remote_attestation import RemoteAttestor

class SGXExposureVerifier:
    def __init__(self, enclave_path="enclaves/exposure_verifier.signed.so"):
        self.enclave = sgx_enclave_lib.SgxEnclave(enclave_path)
        self.attestor = RemoteAttestor()
        
    def verify(self, portfolio: dict, max_exposure: float) -> bool:
        # Perform remote attestation first
        evidence = self.enclave.get_attestation_evidence()
        if not self.attestor.verify_attestation(evidence):
            raise RuntimeError("Enclave attestation failed")
        
        # Prepare portfolio structure for enclave
        portfolio_struct = self._create_portfolio_struct(portfolio)
        
        # Call enclave verification function
        result = self.enclave.call_function(
            b"verify_exposure", 
            ctypes.byref(portfolio_struct),
            ctypes.c_float(max_exposure)
        )
        return result == 0
    
    def _create_portfolio_struct(self, portfolio: dict):
        class Portfolio(ctypes.Structure):
            _fields_ = [
                ("equity_value", ctypes.c_float),
                ("bond_value", ctypes.c_float),
                ("derivatives_value", ctypes.c_float),
                ("cash_value", ctypes.c_float),
                ("total_value", ctypes.c_float),
                ("client_risk_tier", ctypes.c_uint8),
                ("commitment", ctypes.c_ubyte * 32)
            ]
        
        # Create and populate struct
        p = Portfolio()
        p.equity_value = portfolio["equity_value"]
        p.bond_value = portfolio["bond_value"]
        p.derivatives_value = portfolio["derivatives_value"]
        p.cash_value = portfolio["cash_value"]
        p.total_value = portfolio["total_value"]
        p.client_risk_tier = portfolio["client_risk_tier"]
        
        # Generate commitment hash
        import hashlib
        data = bytes(p)[:ctypes.sizeof(Portfolio) - 32]
        commitment = hashlib.sha256(data).digest()
        ctypes.memmove(p.commitment, commitment, 32)
        
        return p