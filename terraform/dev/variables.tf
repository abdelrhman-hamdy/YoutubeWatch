variable "db_username" {
  type = string

}
variable "db_password" {
  type = string
  sensitive = true
}

variable "BUCKET_NAME" {
  type = string
}

variable "YoutupeApi" {
  type = string
  sensitive = true
}

variable "ChannelIDs" {
  type = list(string)
}


variable "email_address" {
  type = string
}

variable "SummrizationApiKey" {
  type = string
  sensitive = true
}


