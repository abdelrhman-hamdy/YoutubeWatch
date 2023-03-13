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
  content=var.ChannelIDs
}

module "SNS" {
  source = "../modules/SNS"
  protocol = "email"
  endpoint  = var.email_address
  
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