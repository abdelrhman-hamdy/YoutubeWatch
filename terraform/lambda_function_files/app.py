import os
from youtupeAPI_handler import get_playlist_ids, get_last_uploaded_vedios
from boto3_handler import get_ssm_parameter, get_latest_app_configuration, push_msg_to_topic
import json
import mysql.connector    
from googleapiclient.discovery import build
import isodate
from youtube_transcript_api import YouTubeTranscriptApi
#Check boto3_handler to understand how these function works

# set the summerization API's HTTP request body and URL
summarize_API_URL='https://api.edenai.run/v2/text/summarize'
payload = {
  "providers": "openai",
  "output_sentences": 3,
  "text": "",
  "language": "en"
}

def lambda_handler(event, context):

    # loading parameters from AWS system manager store parameter
    db_host= get_ssm_parameter('mysql_endpoint')
    db_user= get_ssm_parameter('mysql_username')
    db_pass= get_ssm_parameter('mysql_password')
    api_key= get_ssm_parameter('YoutupeApiKey')
    summ_api_key= get_ssm_parameter('SummrizationApiKey')

    headers = {
        "Content-Type": "application/json",
        "Authorization":f'Bearer {summ_api_key}'
        }

    # Get app configuration from AWS AppConfig
    channelIDs= get_latest_app_configuration('YoutupeWatch','test','ChannelIDs',123)

    #Connect to mysql
    mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass
    )
    mysql_cursor = mydb.cursor()

    #select the database
    mysql_cursor.execute("use YoutubeWatch")

    #intiate youtupe object to use in calling data from the API
    youtube = build("youtube", "v3", developerKey=api_key)


    #get channels playlist 
    playlist_ids= get_playlist_ids(youtube, channelIDs)
    
    #get latest uploaded vedio for each channel
    all_latest_channels_videos= get_last_uploaded_vedios(youtube,playlist_ids)
    
    # preparing insertion sql command
    sql = "INSERT INTO YoutupeChannels (ChannelName,ChannelID,LastUploadedVedioName,LastUploadedVedioID,URL)  VALUES (%s, %s, %s, %s, %s)"
    
    num_of_sent_emails=[]
    
    for channel in all_latest_channels_videos : 
        
        # query to Check if the video exist or not 
        mysql_cursor.execute(f'SELECT * from YoutupeChannels WHERE ChannelID="{channel["channelId"]}" AND LastUploadedVedioID="{channel["vedioId"]}" ')
        
        vedio_exist=mysql_cursor.fetchone()
    
        # if the video not exist , insert it to the databse , and push a massege to SNS
        if vedio_exist is None: 
            val=(channel["channelTitle"],channel["channelId"],channel["vedioTitle"],channel["vedioId"],channel["link"])
            mysql_cursor.execute(sql, val)
            mydb.commit()

            items=YouTubeTranscriptApi.get_transcript(channel["vedioId"])
            for item in items:
                transcript = transcript + item['text']
            payload['text']=transcript
            response = requests.post(summarize_API_URL, json=payload, headers=headers)
            summary = response.json()['openai']['result']

            msg_body= f"Your Favourite Youtuper {channel["channelTitle"]} Has uploaded a new video titled: "{channel["vedioTitle"]}".\n\nA Summary of the video's topic{text} \n\nTo watch it please visit this link {channel["link"]}"
            
            msg_id=push_msg_to_topic('YoutupeWatch',f'New video of {channel["channelTitle"]}',msg_body)
            num_of_sent_emails.append(msg_id)
    
    print( f'a total of {len(num_of_sent_emails)} Emails have been sent ')
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f'a total of {len(num_of_sent_emails)} Emails have been sent ',
        }),
    }
    
