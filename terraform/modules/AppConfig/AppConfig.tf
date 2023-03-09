resource "aws_appconfig_application" "application" {
  name        = var.AppName
  description = "AppConfig  for Application"

  tags = {
    Type = "AppConfig Application"
  }
}

resource "aws_appconfig_environment" "enviroment" {
  name           = var.env
  description    = "AppConfig Production Environment for YoutupeWatch"
  application_id = aws_appconfig_application.application.id

#  monitor {
#    alarm_arn      = aws_cloudwatch_metric_alarm.example.arn
#    alarm_role_arn = aws_iam_role.example.arn
#  }
  tags = {
    Type = "AppConfig Environment"
  }
}


 

resource "aws_appconfig_configuration_profile" "profile" {
  application_id = aws_appconfig_application.application.id
  description    = "Configuration Profile"
  name           = var.profile 
  location_uri   = "hosted"
  #type= "AWS.Freeform"
  #validator {
  #  content = aws_lambda_function.example.arn
  # type    = "LAMBDA"
  # }

}


resource "aws_appconfig_hosted_configuration_version" "content" {
  application_id           = aws_appconfig_application.application.id
  configuration_profile_id = aws_appconfig_configuration_profile.profile.configuration_profile_id
  description              = "Freeform Hosted Configuration Version"
  content_type             = "application/json"

  content = jsonencode({
    "channelIDs" = var.content 
  })
}

resource "aws_appconfig_deployment_strategy" "strategy" {
  name                           = "youtupewatch-deployment-strategy"
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  #growth_type                    = "LINEAR"
  replicate_to                   = "NONE"
}


resource "aws_appconfig_deployment" "deployment" {
  application_id           = aws_appconfig_application.application.id
  configuration_profile_id = aws_appconfig_configuration_profile.profile.configuration_profile_id
  configuration_version    = aws_appconfig_hosted_configuration_version.content.version_number
  deployment_strategy_id   = aws_appconfig_deployment_strategy.strategy.id
  environment_id           = aws_appconfig_environment.enviroment.environment_id 
  depends_on = [
    aws_appconfig_application.application,aws_appconfig_deployment_strategy.strategy,aws_appconfig_configuration_profile.profile,aws_appconfig_environment.enviroment,aws_appconfig_hosted_configuration_version.content
  ]
}






