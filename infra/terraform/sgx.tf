# infra/terraform/sgx.tf
resource "azurerm_attestation_provider" "risk_attestation" {
  name                = "rothschild-risk-attestation"
  resource_group_name = azurerm_resource_group.risk.name
  location           = "switzerlandnorth"

  policy_signing_certificate_data = filebase64("certs/attestation_cert.pem")
}

resource "azurerm_linux_virtual_machine" "sgx_node" {
  name                = "rothschild-sgx-${var.env}"
  size                = "Standard_DC8s_v3" # SGX-enabled
  admin_username      = "sgxadmin"
  
  os_disk {
    storage_account_type = "Premium_LRS"
    security_encryption_type = "VMGuestStateOnly"
  }

  confidential_vm_enabled = true

  # Attach attestation provider
  identity {
    type = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.sgx_identity.id]
  }
}

resource "azurerm_user_assigned_identity" "sgx_identity" {
  name                = "sgx-attestation-identity"
  resource_group_name = azurerm_resource_group.risk.name
  location            = azurerm_resource_group.risk.location
}