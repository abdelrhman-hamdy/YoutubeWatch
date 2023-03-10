resource "aws_ssm_parameter" "secret" {
  name        = "YoutupeApiKey"
  description = "my youtupe api key"
  type        = "SecureString"
  value       = var.api_key

  tags = {
    environment = "production"
  }
} 
