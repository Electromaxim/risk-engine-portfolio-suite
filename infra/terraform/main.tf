module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"
  name    = "risk-engine-vpc"
  cidr    = "10.0.0.0/16"
  
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
}

resource "aws_rds_cluster" "risk_db" {
  cluster_identifier = "risk-engine-rds"
  engine             = "aurora-postgresql"
  database_name      = "riskdb"
  master_username    = var.db_admin
  master_password    = var.db_password # Retrieved from Vault
}

resource "aws_s3_bucket" "market_data" {
  bucket = "rothschild-market-data-${var.env}"
  acl    = "private"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}