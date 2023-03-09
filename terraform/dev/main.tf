terraform {
    required_providers {
      aws = {
	      source = "hashicorp/aws"
	      version = "~> 3.27"
      }
    }
  required_version = ">= 0.14.9"
}

provider "aws" {
    region = "us-east-1"
    profile = "default"
}

module "Mysql" {
  source = "../modules/Mysql"
  db_username=var.db_username
  db_password=var.db_password

}

module "AppConfig" {
  source = "../modules/AppConfig"
  AppName= "YoutupeWatch"
  env= "test"
  profile="ChannelIDs"
  content=["UC9T54M7XBSfc16rsgjAeOBg","UCoOae5nYA7VqaXzerajD0lg" ,"UCck1m7zZdzioiUzqhzpdNPw"]
  
}


#module "s3" {
#  source = "../modules/S3bucket"
#  buckbucketname =  "youtube-wtach-bucket"
#  acl = "private"  
 # src =  "ChannelsID.json" 
 # dest =  "ChannelsID.json"
#}


output "Mysql_endpoint" {
  value = module.Mysql.mysql-database.endpoint
}
