variable "db_username" {
  type = string

}
variable "db_password" {
  type = string
  sensitive = true
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
