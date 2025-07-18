resource "aws_s3_bucket" "risk_audit_logs" {
  bucket = "rothschild-risk-audit-${var.env}"
  
  object_lock_configuration {
    object_lock_enabled = "Enabled"
    rule {
      default_retention {
        mode = "GOVERNANCE"
        years = 7
      }
    }
  }

  versioning {
    enabled = true
  }
}

# infra/terraform/audit_logs.tf - Critical Fix
resource "aws_s3_bucket_object_lock_configuration" "audit_lock" {
  object_lock_enabled = "Enabled"
  rule {
    default_retention {
      mode = "COMPLIANCE"  # Change from GOVERNANCE
      years = 7
    }
  }
}

resource "aws_s3_bucket_policy" "audit_lock_policy" {
  bucket = aws_s3_bucket.risk_audit_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:DeleteObject"
        Resource  = "${aws_s3_bucket.risk_audit_logs.arn}/*"
        Condition = {
          Null = {
            "s3:ObjectLockRemainingRetentionDays" = "true"
          }
        }
      }
    ]
  })
}