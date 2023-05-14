import boto3
import json


# Create boto3 Clients
ssm = boto3.client('ssm')
appconfig = boto3.client('appconfigdata')
sns = boto3.client('sns')
transcribe=boto3.client('transcribe')
s3 = boto3.client('s3')

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

def transcribe_audio(bucket_name,video_id): 
    response = transcribe.start_transcription_job(
    TranscriptionJobName=video_id,
    Media={'MediaFileUri':f's3://{bucket_name}/{video_id}.mp4' },
    MediaFormat='mp4',
     IdentifyLanguage=True
    )

    while True : 
        response =transcribe.list_transcription_jobs(JobNameContains=video_id)
        
        if response['TranscriptionJobSummaries'][0]['TranscriptionJobStatus'] != 'IN_PROGRESS': 
            break
    response=transcribe.get_transcription_job(TranscriptionJobName=video_id)
    output_bucket = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    return output_bucket


def upload_file(audio_path,bucket_name):

    video_id= audio_path.split("/")[-1].split(".")[0]
    with open(audio_path, "rb") as f:

        s3.upload_fileobj(f, bucket_name, f'{video_id}.mp4')
