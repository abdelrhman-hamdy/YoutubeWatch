import os
from googleapiclient.discovery import build 
from IPython.display import JSON
import isodate

#api_key=""
#api_service_name = "youtube"
#api_version = "v3"
#channelIDs=["UCoOae5nYA7VqaXzerajD0lg","UCboi9tFaUpreNfGMBoZ339A","UCJQJAI7IjbLcpsjWdSzYz0Q","UCJ24N4O0bP7LGLBDvye7oCA","UCWpr8yIhv8wOvdR27W2Mybw"]


# Get credentials and create an API client
#youtube = build(api_service_name, api_version, developerKey=api_key)


def get_playlist_ids(youtube, channel_ids):
    request = youtube.channels().list(part="snippet,contentDetails,statistics", id=",".join(channel_ids))
    response = request.execute()
    PlayListIDs=[]
    for item in response['items']: 
        PlayListIDs.append(item['contentDetails']['relatedPlaylists']['uploads'])
    return PlayListIDs
    



def get_last_uploaded_vedios(youtube,playlist_ids):
    lists_of_latest_vedios=[]
    count=0

    for playlistID in playlist_ids :
        
        request = youtube.playlistItems().list(maxResults=50,part='contentDetails',playlistId=playlistID)
        response = request.execute()

        for vedio in response['items'] :
            vedioId=vedio['contentDetails']['videoId']
            request=youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id = vedioId
            )
            response = request.execute()
            vedioTitle=response['items'][0]['snippet']['title']
            channelId=response['items'][0]['snippet']['channelId']
            channelTitle=response['items'][0]['snippet']['channelTitle']
            dur=isodate.parse_duration(str(response['items'][0]['contentDetails']['duration']))
            if int(dur.total_seconds()) > 100 :
                link= f'https://www.youtube.com/watch?v={vedioId}'
                lists_of_latest_vedios.append([channelTitle,channelId,vedioTitle,vedioId,link])
                break
            
    return lists_of_latest_vedios



