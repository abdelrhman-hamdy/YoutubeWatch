terraform {
    required_providers {
      aws = {
	      source = "hashicorp/aws"
	      version = "~> 4.5"
      }
    }
  required_version = ">= 0.14.9"
}

provider "aws" {
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
  content=["UC9T54M7XBSfc16rsgjAeOBg","UCEHvaZ336u7TIsUQ2c6SAeQ","UCoOae5nYA7VqaXzerajD0lg" ,"UCck1m7zZdzioiUzqhzpdNPw","UCpui0-2JqcAcII4ybpB1q3w"]
}

module "SNS" {
  source = "../modules/SNS"
  protocol = "email"
  endpoint  = "abdelrhman.hamdy1969@gmail.com"
  
}

module "ParameterStore" {
  source = "../modules/ParameterStore"
  api_key= var.YoutupeApi
  db_host=module.Mysql.mysql-database.address
  db_user=var.db_username
  db_pass=var.db_password
  depends_on = [
    module.Mysql
  ]
}

#module "s3" {
#  source = "../modules/S3bucket"
#  buckbucketname =  "youtube-wtach-bucket"
#  acl = "private"  
 # src =  "ChannelsID.json" 
 # dest =  "ChannelsID.json"
#}



module "cloudwatch" {
  source = "../modules/cloudwatch"
  lambda_arn=module.lambda.YoutubeWatch-lambda.arn
  lambda_name=module.lambda.YoutubeWatch-lambda.function_name
  depends_on = [
    module.lambda
  ]
}

module "lambda" {
  source = "../modules/Lambda"
}


