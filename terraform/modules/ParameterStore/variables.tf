variable "api_key" {
  type=string
  sensitive = true
}

variable "SummrizationApiKey" {
  type = string
  sensitive = true
}
variable "BUCKET_NAME" {
  type = string
}



variable "db_host" {
  type=string
  sensitive = true
}
variable "db_user" {
  type=string
  sensitive = true
}
variable "db_pass" {
  type=string
  sensitive = true
}
