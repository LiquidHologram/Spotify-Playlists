import requests
import datetime
#from urllib.parse import urlencode
import base64
import json
#import pandas as pd
import creds
# import googleapiclient.discovery


client_id = creds.spotify_client_id
client_secret = creds.spotify_client_secret

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def get_token_data(self):
        return {
            'grant_type': 'client_credentials'
        }
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # Seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

#def youtube_playlisting():
    # This will open users youtube playlist
    # Add users spotify playlist/youtube results to a playlist on youtube

# api_service_name = "youtube"
# api_version = "v3"
# client_secrets_file = "client_secret_Gapi.json"
# api_key = creds.youtube_api_key

# For future youtube integration
# youtube = googleapiclient.discovery.build(
#     api_service_name, api_version, developerKey=api_key)

client = SpotifyAPI(client_id, client_secret)
client.perform_auth()

access_token = client.access_token

headers = {
    "Authorization": f"Bearer {access_token}"
}
params = {
    "market": "ES",
    "fields": "next,items(track(name, artists))",
    "limit": 100,
    "offset": 0
}

#playlist_id = input('Please add playlist UID: ') # "Sample: 25gTxVbo0CTsMEjx8clehi" This can be made into a user input for their spotify playlist
track_endpoint = f'https://api.spotify.com/v1/playlists/25gTxVbo0CTsMEjx8clehi/tracks?offset=0&limit=100&locale=en-US,en;q=0.5'



songs = []
offset = 0
limit = 100

# Loops through the api pages to get all songs
while track_endpoint:
    # print('----')

    response = requests.get(track_endpoint, params=params, headers=headers)
    data = response.json()

    songs.append(data)

    track_endpoint = data['next']

# Saves tracknames to json file
with open(f'spotify_playlist.json', 'w') as outfile:
    datadump = json.dump(songs, outfile, indent=2, sort_keys=True)

try:
    with open(f'spotify_playlist.json') as f:
        datadump = json.load(f)

except FileNotFoundError:
    print('The specified file could not be found.')
except json.JSONDecodeError as e:
    print(f'There was a problem decoding the JSON data: {e}')
else:
    # Loop through all pages of the playlists via datadump
    for i in range(len(datadump)):
        track_names = [item['track']['name'] for item in datadump[i]['items']]
        artist_name = [item['track']['artists'][0]['name'] for item in datadump[i]['items']]

        # Print track name and artist names together
        for track, artist in zip(track_names, artist_name):
            print(f'{track} - {artist}')



#Youtube portion
'''
video_ids = []

for x, y in zip(track_names, artist_name):
    playlist_result = (f"{x} - {y} Music Video")
    #print(playlist_result)

    search_response = youtube.search().list(
        q = playlist_result,
        type = 'video',
        part = 'id',
        maxResults = 1
    ).execute()

    video_id = search_response['items'][0]['id']['videoId']

    video_ids.append(video_id)

    print(f'Video ID for {playlist_result}: {video_id}')
'''
# test1 = playlist_output["items"]
# # test2 = list(test1)[0]
# # test3 = test2[1:-1]
# print(test1)