from pytube import YouTube
import boto3
import concurrent.futures
import time 
from youtupeAPI_handler import get_playlist_ids, get_last_uploaded_vedios
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import mysql.connector   
import threading 
import requests
from boto3_handler import get_ssm_parameter, get_latest_app_configuration, push_msg_to_topic, transcribe_audio, upload_file
import os
import json



# create lock for locking access the database to only one thread at a time 
lock = threading.Lock()
def check_video_existence(channel,connection_pool): 
    # query to Check if the video exist or not 
    lock.acquire()
    mysql = connection_pool.get_connection()
    mysql_cursor=mysql.cursor()

    sql = "INSERT INTO YoutupeChannels (ChannelName,ChannelID,LastUploadedVedioName,LastUploadedVedioID,URL)  VALUES (%s, %s, %s, %s, %s)"
    mysql_cursor.execute(f'SELECT * from YoutupeChannels WHERE ChannelID="{channel["channelId"]}" AND LastUploadedVedioID="{channel["vedioId"]}" ')
    
    vedio_exist=mysql_cursor.fetchone()
    if vedio_exist is None: 

        val=(channel["channelTitle"],channel["channelId"],channel["vedioTitle"],channel["vedioId"],channel["link"])
        mysql_cursor.execute(sql, val)
        mysql.commit()
        mysql.close()
        lock.release()
        return channel 
    
    mysql.close()
    lock.release()

def get_audio(video_id):
    yt=YouTube(f'https://www.youtube.com/watch?v={video_id}') 
    audio_streams= yt.streams.filter(only_audio=True,file_extension='mp4')
    stream=audio_streams.first()
    path=stream.download(filename=f"{video_id}.mp4")
    return path


def get_summary(url,summarize_API_URL,payload,headers): 
    response=requests.get(url)
    transcript=response.json()['results']['transcripts'][0]['transcript']
    language= response.json()['results']['language_code']
    video_id= response.json()['jobName']
    payload['text']=transcript
    payload['language']=language
    
    response = requests.post(summarize_API_URL, json=payload, headers=headers)
    output = response.json()
    if output['openai']['status'] == 'success':
        summary = response.json()['openai']['result']
        return {'summary':summary,'video_id':video_id}
    return {'video_id':video_id}
    

def get_video_info_by_id(video_id,new_videos):
    for video in new_videos: 
        if video_id == video['vedioId']:
            return video 
   

def lambda_handler(event, context):


    # Get all parameters
    db_host= get_ssm_parameter('mysql_endpoint')
    db_user= get_ssm_parameter('mysql_username')
    db_pass= get_ssm_parameter('mysql_password')
    DEVELOPER_KEY = get_ssm_parameter('YoutupeApiKey')
    openai_key = get_ssm_parameter('SummrizationApiKey')
    channel_ids= get_latest_app_configuration('YoutupeWatch','test','ChannelIDs',123)
    bucket_name=get_ssm_parameter('BUCKET_NAME')

    # create a pool of mysql connections
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name='YoutubeWatch',
        pool_size=10,
        user=db_user,
        password=db_pass,
         host=db_host,
        database='YoutubeWatch'
    )


    # create youtube client API
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


    # set AI Summarization API's info
    summarize_API_URL='https://api.edenai.run/v2/text/summarize'
    payload = {
      "providers": "openai",
      "output_sentences": 3,
      "text": "",
      "language": ""
    }
    headers = {
      "Content-Type": "application/json",
      "Authorization":f'Bearer {openai_key}'
    }


    # get all latest uploaded videos 
    print('Get Latest Uploaded Videos...')
    playlist_ids= get_playlist_ids(youtube,channel_ids )
    latest_videos= get_last_uploaded_vedios(youtube,playlist_ids)

    
    # check if the video exist in the database
    print('Checking Against database...')
    new_videos=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=[]
        for channel in latest_videos :
            result=executor.submit(check_video_existence,channel,connection_pool)
            results.append(result)

        for result in concurrent.futures.as_completed(results): 
            new_videos.append(result.result())

    print('Checking Completed')


    # exit from the code if Everything is up-to-date
    if all( video is None for video in new_videos ): 
        print('Everything is up-to-date')
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": 'Everything is up-to-date',
        }),
    }


    # get the video IDs of all new videos to download its audio
    videos_ids=[]
    for video in new_videos:
        if video is None : 
            continue
        videos_ids.append(video['vedioId'])

    print('Download audios of the new videos....')
    # download audios for new videos 
    audio_paths=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:

        results=executor.map(get_audio,videos_ids)
    for audio_path in results:
        audio_paths.append(audio_path)

    print('Uploading the Audios to S3....')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for audio_path in audio_paths :
            results=executor.submit(upload_file,audio_path,bucket_name)

    print('The Audios has been uploaded ...')

    print('Transcribe the Audios..')
    audios_urls=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=[]
        for video_id in videos_ids :
            result=executor.submit(transcribe_audio,bucket_name,video_id)
            results.append(result)

        for result in concurrent.futures.as_completed(results): 
            audios_urls.append(result.result())

    print('Transcribed Finished successfully, the transcribed files are ready for Download')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=[]
        for url in audios_urls : 
            result=executor.submit(get_summary,url,summarize_API_URL,payload,headers)
            results.append(result)
        summaries_videos_ids=[]
        for result in concurrent.futures.as_completed(results): 
            summaries_videos_ids.append(result.result())

    print('Videos\' summaries are done')

    num_of_sent_emails=[]
    for summary_videoid in summaries_videos_ids: 

        video=get_video_info_by_id(summary_videoid['video_id'],new_videos)
        if 'summary' not in summary_videoid  :
            msg_body= f'Your Favourite Youtuper "{video["channelTitle"]}" Has uploaded a new video titled: "{video["vedioTitle"]}".\n\nTo watch it please visit this link {video["link"]}'
        else : 
            msg_body= f'Your Favourite Youtuper "{video["channelTitle"]}" Has uploaded a new video titled: "{video["vedioTitle"]}".\n\nA Summary of the video\'s topic: { summary_videoid["summary"] } \n\nTo watch it please visit this link {video["link"]}'
        msg_id=push_msg_to_topic('YoutupeWatch',f'New video of {video["channelTitle"]}',msg_body)
        num_of_sent_emails.append(msg_id)


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f'a total of {len(num_of_sent_emails)} Emails have been sent ',
        }),
    }
