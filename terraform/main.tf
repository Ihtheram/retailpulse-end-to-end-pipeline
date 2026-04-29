# ──────────────────────────────────────────────
# terraform Main
# ──────────────────────────────────────────────

terraform {
  
  required_version = ">= v1.14.9"
  
  required_providers {

    # Go to https://registry.terraform.io/ -> "Browse Providers" -> "Use Provider" (top right)

    aws = {

      # https://registry.terraform.io/providers/hashicorp/aws/latest -> "Use Provider" (top right)

      source  = "hashicorp/aws"
      version = "~> 5.0"
        
      # "~> 5.0" - 5.x only, not 6.0+
      # ">= 5.0" - anything 5.0 or newer including major versions
      # "= 5.94.0" - exact version, no flexibility
    }
    databricks = {
      
      # https://registry.terraform.io/providers/databricks/databricks/latest -> "Use Provider" (top right)
    
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
  
}



# ──────────────────────────────────────────────
# Resource
# ──────────────────────────────────────────────

resource "aws_s3_bucket" "raw_data" {
  bucket = var.bucket_name
}
