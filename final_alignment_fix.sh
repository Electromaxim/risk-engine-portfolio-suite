#!/bin/bash
# final_alignment_fix.sh

# 1. Standardize API error formats
find services -name "*.py" -exec sed -i '
  s/return {"error": "\(.*\)"}/return {"error_code": "E_UNCLASSIFIED", "message": "\1", "trace_id": generate_trace_id()}/g
' {} +

# 2. Enforce common SGX header
for file in services/compliance-security/sgx/enclaves/*; do
  if ! grep -q "#include \"common.h\"" "$file"; then
    sed -i '1i #include "common.h"' "$file"
  fi
done

# 3. Normalize FINMA rule thresholds
awk -i inplace '
  /equity_limit/ {gsub(/0\.2[0-9]/, "0.25")}
  /derivatives_limit/ {gsub(/0\.1[0-9]/, "0.15")}
  {print}
' services/compliance-security/rule_engine/*.py

# 4. Update Terraform encryption flags
find infra/terraform -name "*.tf" -exec sed -i '
  s/security_encryption_type = .*/security_encryption_type = "VMGuestStateOnly"/g
  s/confidential_vm_enabled = .*/confidential_vm_enabled = true/g
' {} +

# 5. Verify and commit changes
terraform validate infra/terraform
pytest tests/
git commit -am "Final consistency alignment for production"