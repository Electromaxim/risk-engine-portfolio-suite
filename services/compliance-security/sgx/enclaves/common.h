// services/compliance-security/sgx/enclaves/common.h
#ifndef COMMON_H
#define COMMON_H

#include <sgx.h>
#include <stdint.h>

// Standardized portfolio structure
typedef struct {
    float equity_value;
    float bond_value;
    float derivatives_value;
    float cash_value;
    float total_value;
    uint8_t client_risk_tier;
    uint8_t commitment[32];  // SHA-256 hash
} Portfolio;

// Standardized verification result codes
#define VERIFICATION_SUCCESS 0
#define ERR_HASH_MISMATCH 1
#define ERR_EQUITY_CONCENTRATION 2
#define ERR_DERIVATIVES_CONCENTRATION 3
#define ERR_EXPOSURE_LIMIT 4

#endif