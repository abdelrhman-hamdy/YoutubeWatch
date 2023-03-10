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



api_key= get_ssm_parameter('YoutupeApiKey')
db_host= get_ssm_parameter('mysql_endpoint')
db_user= get_ssm_parameter('mysql_username')
db_pass= get_ssm_parameter('mysql_password')

channelIDs= get_latest_app_configuration('YoutupeWatch','test','ChannelIDs',123)


print(api_key,db_host,db_user,db_pass)


mydb = mysql.connector.connect(
  host=db_host,
  user=db_user,
  password=db_pass
)

mysql_cursor = mydb.cursor()
mysql_cursor.execute("use YoutubeWatch")

youtube = build("youtube", "v3", developerKey=api_key)

playlist_ids= get_playlist_ids(youtube, channelIDs)

all_channels_data= get_last_uploaded_vedios(youtube,playlist_ids)

for channel in all_channels_data : 
    mysql_cursor.execute(f'SELECT * from YoutupeChannels WHERE ChannelID="{channel[1]}" AND LastUploadedVedioID="{channel[3]}" ')
    vedio_exist=mysql_cursor.fetchone()
    print("...................",vedio_exist)
    if vedio_exist is None: 
        mysql_cursor.execute(f'INSERT INTO YoutupeChannels (ChannelName,ChannelID,LastUploadedVedioName,LastUploadedVedioID,URL) VALUES  ("{channel[0]}","{channel[1]}","{channel[2]}","{channel[3]}","{channel[4]}") ')

mysql_cursor.execute(f'SELECT * from YoutupeChannels ')

rows=mysql_cursor.fetchall()
for row in rows : 
    print(row)

    
