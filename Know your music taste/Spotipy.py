## Create account https://developer.spotify.com/dashboard/login  to get the API key

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import display
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


SPOTIFY_CLIENT_ID = ''  # Your Spotify Client ID
SPOTIFY_CLIENT_SECERET = ''  # Your Spotify Client Seceret ID

scope = "user-private-read"
cliend_cre = SpotifyClientCredentials(SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECERET)
sp = spotipy.Spotify(client_credentials_manager=cliend_cre)

playlist_id = ""  # Playlist ID
res = sp.playlist(playlist_id)

ids=[]

for item in res['tracks']['items']:
        track = item['track']['id']
        ids.append(track)
        
song_meta={'id':[],'album':[], 'name':[], 
        'artist':[],'explicit':[],'popularity':[]
        }

for song_id in ids:
        # get song's meta data
        meta = sp.track(song_id)
        
        # song id
        song_meta['id'].append(song_id)

        # album name
        album=meta['album']['name']
        song_meta['album']+=[album]

        # song name
        song=meta['name']
        song_meta['name']+=[song]
        
        # artists name
        s = ', '
        artist=s.join([singer_name['name'] for singer_name in meta['artists']])
        song_meta['artist']+=[artist]
        
        # explicit: lyrics could be considered offensive or unsuitable for children
        explicit=meta['explicit']
        song_meta['explicit'].append(explicit)
        
        # Popularity of Song
        popularity=meta['popularity']
        song_meta['popularity'].append(popularity)

song_meta_df=pd.DataFrame.from_dict(song_meta)

# check the song feature
features = sp.audio_features(song_meta['id'])
# change dictionary to dataframe
features_df=pd.DataFrame.from_dict(features)

# convert milliseconds to mins
# duration_ms: The duration of the track in milliseconds.
# 1 min = 60 sec = 60 × 1000 millisec = 60,000 ms
features_df['duration_ms']=features_df['duration_ms']/60000

# combine two dataframe
final_df=song_meta_df.merge(features_df)


### Now making a final DataFrame for analysing your music taste in your playlist

music = features_df[['danceability', 'energy', 'loudness', 'speechiness','acousticness', 
                'instrumentalness', 'liveness','valence', 'tempo','duration_ms']]


min_max_scaler = MinMaxScaler()
music.loc[:]=min_max_scaler.fit_transform(music.loc[:])

fig=plt.figure(figsize=(12,8))
pi = 3.14
categories=list(music.columns)
N=len(categories)

value=list(music.mean())

value+=value[:1]

angles=[n/float(N)*2*pi for n in range(N)]
angles+=angles[:1]

# plot
plt.polar(angles, value)
plt.fill(angles,value,alpha=0.3)

plt.xticks(angles[:-1],categories, size=15)
plt.yticks(color='grey',size=15)
plt.show()