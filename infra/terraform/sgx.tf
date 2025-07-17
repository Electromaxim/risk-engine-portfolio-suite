resource "azurerm_linux_virtual_machine" "sgx_node" {
  name                = "rothschild-sgx-${var.env}"
  size                = "Standard_DC8s_v3" # SGX-enabled
  admin_username      = "sgxadmin"
  
  os_disk {
    storage_account_type = "Premium_LRS"
    security_encryption_type = "VMGuestStateOnly"
  }

  confidential_vm_enabled = true
}