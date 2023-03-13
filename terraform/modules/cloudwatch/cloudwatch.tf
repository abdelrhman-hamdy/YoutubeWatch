resource "aws_cloudwatch_event_rule" "every_60_minutes" {
    name = "trigger-lambda-every-60-mins"
    description = "Trigger Youtubewatch lambda function every 60 mins"
    schedule_expression = "rate(60 minutes)"
}

resource "aws_cloudwatch_event_target" "trigger_lambda_every_60_minutes" {
    rule = aws_cloudwatch_event_rule.every_60_minutes.name
    target_id = "TriggerLambda"
    arn =  var.lambda_arn 
}

resource "aws_lambda_permission" "allow_cloudwatch_to_trigger_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = var.lambda_name 
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.every_60_minutes.arn
}
