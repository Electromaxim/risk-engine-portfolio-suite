#!/bin/bash
# validate_structure.sh

# Define the canonical structure
declare -A canonical_dirs=(
  ["infra/terraform"]=1
  ["services/risk-engine-core/models"]=1
  ["services/compliance-security/sgx"]=1
  # Add all other directories...
)

# Check for misplaced files
find . -type f | while read file; do
  parent_dir=$(dirname "$file")
  if [[ ! -v canonical_dirs["$parent_dir"] ]]; then
    echo "STRUCTURE ERROR: $file in invalid location"
    echo "Should be moved to:"
    grep -r -l --include="*.py" "$(basename "$file")" . | grep -v "$parent_dir"
  fi
done

# Check for duplicate implementations
find . -name "*.py" -exec grep -H -n "class " {} \; | 
  awk -F: '{print $3}' | sort | uniq -c | 
  awk '$1>1 {print "DUPLICATE CLASS: " $2}'