#include <sgx_urts.h>
#include "exposure_verifier.h"
#include <openssl/sha.h>

sgx_status_t verify_exposure(sgx_enclave_id_t eid, Portfolio *portfolio, float max_exposure) {
    sgx_status_t ret;
    
    // 1. Validate portfolio commitment
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((const unsigned char*)portfolio, sizeof(Portfolio), hash);
    
    if (memcmp(hash, portfolio->commitment, SHA256_DIGEST_LENGTH) != 0) {
        return SGX_ERROR_INVALID_PARAMETER;
    }
    
    // 2. FINMA concentration rules (Art. 42)
    float total = portfolio->equity_value + portfolio->bond_value + 
                  portfolio->derivatives_value + portfolio->cash_value;
    
    if (portfolio->equity_value > total * 0.25f || 
        portfolio->derivatives_value > total * 0.15f) {
        return SGX_ERROR_INVALID_PARAMETER;
    }
    
    // 3. Client exposure limit
    if (total > max_exposure) {
        return SGX_ERROR_INVALID_PARAMETER;
    }
    
    return SGX_SUCCESS;
}