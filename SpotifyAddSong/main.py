import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


URL = "https://www.billboard.com/charts/hot-100"


spotify_id = "secret"
spotify_secret = "secret"
redirect_uri = "http://localhost:8888/callback"



header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
date = input("what year you would like to travel to? Format: YYYY-MM-DD")
response = requests.get(url=f"{URL}/{date}",headers=header)
yc_web_page = response.text


soup = BeautifulSoup(yc_web_page,'html.parser',)
# divs = soup.find_all("div", class_="o-chart-results-list-row-container")
#
# sounds_list = []
#
# for div in divs:
#     title_tag = div.find("h3", class_="c-title")
#     if title_tag:
#         sounds_list.append(title_tag.text.strip())
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

print(song_names)

sp_oauth = SpotifyOAuth(
    client_id=spotify_id,
    client_secret=spotify_secret,
    redirect_uri=redirect_uri,
    # scope="playlist-modify-private"
)
sp = spotipy.Spotify(auth_manager=sp_oauth)

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"Playlist {date}",
    description="New playlist description",
    public=False
)
playlist_id = playlist["id"]
print(f"Created playlist with ID: {playlist_id}")

print("Playlist created successfully:", playlist)

track_ids = []

for song in song_names:
    track_name = song
    results = sp.search(q=track_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track_id = results["tracks"]["items"][0]["id"]
        track_ids.append(track_id)
        print(f"Found track '{song}' with ID: {track_id}")


if track_ids:
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=track_ids)
    print("Tracks added successfully to the playlist!")
else:
    print("No tracks found to add to the playlist.")