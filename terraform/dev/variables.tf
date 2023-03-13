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
  default = ["UC9T54M7XBSfc16rsgjAeOBg","UCEHvaZ336u7TIsUQ2c6SAeQ","UCoOae5nYA7VqaXzerajD0lg" ,"UCck1m7zZdzioiUzqhzpdNPw","UCpui0-2JqcAcII4ybpB1q3w"]
}


variable "email_address" {
  type = string
  default = "abdelrhman.hamdy1969@gmail.com"
}
