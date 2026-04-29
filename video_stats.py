import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')

API_KEY = os.getenv("API_KEY")
CHANNELS = ['PapaMeat', 'coldones', 'CalebHammer']

def get_playlist_id(channel_handle):
    #Creating the request urls for the channel playlist
    try:
        channel_req_url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}'

        #Requesting the channel playlist id information from the YouTube API
        channel_response = requests.get(channel_req_url)

        #Getting the channel playlist
        channel_data = channel_response.json()
        channel_playlistId = channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        return channel_playlistId
    
    except requests.exceptions.RequestException as e:
        raise e
    
def get_video_ids(playlist_id):
    video_ids = []
    pageToken = None
    playlist_request_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}'
    try:
        while True: 
            
            url = playlist_request_url

            if pageToken:
                url += f'&pageToken={pageToken}'
            
            response = requests.get(url)

            response.raise_for_status()

            data=response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            
            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

    except requests.exceptions.RequestException as e:
        raise e   
    
    return video_ids

if __name__ == "__main__":
    channel_playlist_dict = {}
    channel_video_dict = {}
    for channel in CHANNELS:
        channel_playlist_dict[channel] = (get_playlist_id(channel))
        channel_video_dict[channel] = get_video_ids(channel_playlist_dict[channel])
        print(len(channel_video_dict[channel]))