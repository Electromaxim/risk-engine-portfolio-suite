# infra/terraform/audit_logs.tf
resource "aws_s3_bucket" "risk_audit_logs" {
  bucket = "rothschild-risk-audit-${var.env}"
  
  object_lock_configuration {
    object_lock_enabled = "Enabled"
    rule {
      default_retention {
        mode = "COMPLIANCE"  # Changed from GOVERNANCE
        years = 7
      }
    }
  }

  versioning {
    enabled = true
  }

  # Add FINMA-mandeted encryption
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# Enable MFA delete protection
resource "aws_s3_bucket_versioning" "audit_versioning" {
  bucket = aws_s3_bucket.risk_audit_logs.id
  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Enabled"
  }
}