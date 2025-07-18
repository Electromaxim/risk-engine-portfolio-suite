# infra/terraform/validate.tf
resource "null_resource" "consistency_check" {
  triggers = {
    # Force revalidation on every run
    timestamp = timestamp()
  }

  provisioner "local-exec" {
    command = <<EOT
      # Verify all SGX nodes use same image
      IMAGES=$(terraform output sgx_node_image | uniq | wc -l)
      if [ "$IMAGES" -ne 1 ]; then
        echo "SGX NODE INCONSISTENCY: Multiple images detected"
        exit 1
      fi

      # Verify encryption is enabled everywhere
      grep -r "encryption" --include=*.tf . | grep -v "true" && \
        echo "ENCRYPTION INCONSISTENCY" && exit 1
    EOT
  }
}