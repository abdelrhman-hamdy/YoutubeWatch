import json
from googleapiclient.discovery import build
from IPython.display import JSON
import isodate
import os
from youtupeAPI import get_playlist_ids, get_last_uploaded_vedios


channelIDs=["UCoOae5nYA7VqaXzerajD0lg","UCboi9tFaUpreNfGMBoZ339A"]
youtube = build("youtube", "v3", developerKey=api_key)


def lambda_handler(event, context):

    playlist_ids= get_playlist_ids(youtube, channelIDs)
    lists_of_videos=get_last_uploaded_vedios(youtube,playlist_ids)
    

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f'{lists_of_videos}',
            # "location": ip.text.replace("\n", "")
        }),
    }
