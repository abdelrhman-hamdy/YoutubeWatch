import boto3
import json


# Create boto3 Clients
ssm = boto3.client('ssm')
appconfig = boto3.client('appconfigdata')
sns = boto3.client('sns')


# Functions to handle interacting with AWS services using boto3 
#  Get parameter value from "System manager Store parameter" using parameter name
def get_ssm_parameter(parameter_name):
    response = ssm.get_parameter(Name=parameter_name,WithDecryption=True)
    return response['Parameter']['Value']


# Get latest application configuration from Appconfig
def get_latest_app_configuration(app_name,env,profile,poll_int):
    
    appconfig_response = appconfig.start_configuration_session(
        ApplicationIdentifier= app_name,
        EnvironmentIdentifier= env,
        ConfigurationProfileIdentifier= profile,
        RequiredMinimumPollIntervalInSeconds= poll_int
    )
    appconfig_token=appconfig_response['InitialConfigurationToken']
    channelIDs = appconfig.get_latest_configuration(ConfigurationToken=appconfig_token)
    return json.loads(channelIDs['Configuration'].read().decode("utf-8"))['channelIDs']

# Load parameters from AWS parameter store
def push_msg_to_topic(topic_name,subject,msg_body ):
    topic_metadata = sns.create_topic(Name=topic_name)
    topic_arn= topic_metadata['TopicArn']
    MessageId = sns.publish(TopicArn=topic_arn, Message=msg_body, Subject=subject )['MessageId']
    return MessageId
