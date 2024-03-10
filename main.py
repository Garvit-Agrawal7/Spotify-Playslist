import os
from pprint import pprint
from bs4 import BeautifulSoup
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

client_id = os.environ['SPOTIFY_ID']
client_secret = os.environ['CLIENT_SECRET']
site = "https://www.billboard.com/charts/hot-100/"

date = input("Which day do you want to travel? Type the date in YYYY-MM-DD format: ")
site = site + date

soup = BeautifulSoup(requests.get(site).text, "html.parser")
sp = Spotify(oauth_manager=SpotifyOAuth(
    client_id,
    client_secret,
    redirect_uri='http://example.com',
    cache_path='token.txt',
    username=os.environ['USERNAME'],
    scope="playlist-modify-private"
))

tracks_elements = soup.select("li ul li h3")
tracks = [track.getText().strip("\n\t") for track in tracks_elements]

user_id = sp.current_user()["id"]

songs = []
year = date.split("-")[0]
for track in tracks:
    song = sp.search(q=f"track:{track}%20year:{year}", type='track')
    try:
        uri = song["tracks"]["items"][0]["uri"]
        songs.append(uri)
    except IndexError:
        print(f"{track}: Song not found!")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
pprint(playlist)
sp.playlist_add_items(playlist_id=playlist['id'], items=songs)
