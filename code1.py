from googleapiclient.discovery import build
from IPython.display import JSON
import isodate
import os
from youtupeAPI_handler import get_playlist_ids, get_last_uploaded_vedios
#from boto3_handler import get_ssm_parameter, get_latest_app_configuration
import json
import boto3
import mysql.connector    

ssm = boto3.client('ssm')
appconfig = boto3.client('appconfigdata')
sns = boto3.client('sns')

def get_ssm_parameter(parameter_name):
    response = ssm.get_parameter(Name=parameter_name,WithDecryption=True)
    return response['Parameter']['Value']

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


def push_msg_to_topic(topic_name,subject,msg_body ):
    topic_metadata = sns.create_topic(Name=topic_name)
    topic_arn= topic_metadata['TopicArn']
    MessageId = sns.publish(TopicArn=topic_arn, Message=msg_body, Subject=subject )['MessageId']
    return MessageId



# Load parameters from AWS parameter store
api_key= get_ssm_parameter('YoutupeApiKey')
db_host= get_ssm_parameter('mysql_endpoint')
db_user= get_ssm_parameter('mysql_username')
db_pass= get_ssm_parameter('mysql_password')


# Get app configuration from AWS AppConfig
channelIDs= get_latest_app_configuration('YoutupeWatch','test','ChannelIDs',123)

#Connect to mysql 
mydb = mysql.connector.connect(
  host=db_host,
  user=db_user,
  password=db_pass
)
mysql_cursor = mydb.cursor()
mysql_cursor.execute("use YoutubeWatch")
sql = "INSERT INTO YoutupeChannels (ChannelName,ChannelID,LastUploadedVedioName,LastUploadedVedioID,URL)  VALUES (%s, %s, %s, %s, %s)"
youtube = build("youtube", "v3", developerKey=api_key)

#get channels playlist 
playlist_ids= get_playlist_ids(youtube, channelIDs)

#get latest uploaded vedio for each channel
all_latest_videos= get_last_uploaded_vedios(youtube,playlist_ids)

num_of_msg=[]
for channel in all_latest_videos : 
    mysql_cursor.execute(f'SELECT * from YoutupeChannels WHERE ChannelID="{channel["channelId"]}" AND LastUploadedVedioID="{channel["vedioId"]}" ')
    vedio_exist=mysql_cursor.fetchone()
    if vedio_exist is None: 
        #mysql_cursor.execute(f'INSERT INTO YoutupeChannels (ChannelName,ChannelID,LastUploadedVedioName,LastUploadedVedioID,URL) VALUES  ("{channel["channelTitle"]}","{channel["channelId"]}","{channel["vedioTitle"]}","{channel["vedioId"]}","{channel["link"]}") ')
        val=(channel["channelTitle"],channel["channelId"],channel["vedioTitle"],channel["vedioId"],channel["link"])
        mysql_cursor.execute(sql, val)
        mydb.commit()

        msg_body= f'Your Favourite Youtuper {channel["channelTitle"]} Has uploaded a new video titled: "{channel["vedioTitle"]}". To watch it please visit this link {channel["link"]}'
        
        msg_id=push_msg_to_topic('user-updates-YoutupeWatch-topic',f'New video of {channel["channelTitle"]}',msg_body)
        num_of_msg.append(msg_id)

print( f'a total of {len(num_of_msg)} Emails have been sent ')