resource "aws_ssm_parameter" "api_key" {
  name        = "YoutupeApiKey"
  description = "my youtupe api key"
  type        = "SecureString"
  value       = var.api_key

} 
resource "aws_ssm_parameter" "db_host" {
  name        = "mysql_endpoint"
  description = "mysql endpoint"
  type        = "String"
  value       = var.db_host

} 
resource "aws_ssm_parameter" "db_user" {
  name        = "mysql_username"
  description = "mysql username"
  type        = "String"
  value       = var.db_user

} 
resource "aws_ssm_parameter" "db_pass" {
  name        = "mysql_password"
  description = "mysql password"
  type        = "SecureString"
  value       = var.db_pass

} 
