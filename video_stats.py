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


if __name__ == "__main__":
    channel_playlist_dict = {}
    for channel in CHANNELS:
        channel_playlist_dict[channel] = (get_playlist_id(channel))
    print(channel_playlist_dict)