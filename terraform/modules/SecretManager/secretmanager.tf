
# Creating a AWS secret for database master account (Masteraccoundb) 

# Creating a AWS secret versions for database master account (Masteraccoundb)
resource "aws_secretsmanager_secret" "YouTupeApi" {
   name = "youtupeapikey"
}
  

resource "aws_secretsmanager_secret_version" "version" {
  secret_id = aws_secretsmanager_secret.YouTupeApi.id
  secret_string = var.api_key
}
 
# Importing the AWS secrets created previously using arn.
 
data "aws_secretsmanager_secret" "YouTupeApi" {
  arn = aws_secretsmanager_secret.YouTupeApi.arn
}
 
 Importing the AWS secret version created previously using arn.
 
data "aws_secretsmanager_secret_version" "creds" {
  secret_id = data.aws_secretsmanager_secret.YouTupeApi.arn
  depends_on = [
    aws_secretsmanager_secret_version.version
  ]
}
