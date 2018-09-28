from flask import Flask, render_template, url_for, flash, redirect
from flask_socketio import SocketIO, emit, send
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from imports.get_playlists import *
from imports.get_artist_songs import *
from imports.consolidated_playlist_artists import *
from imports.get_recommendations import *
from imports.setup_dataframes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '36363bab19a8b9f255028be3ce336fdd'
socketio = SocketIO(app)

# Sets my id, secret, and redicret url
client_id='278b086924c946fdbe16325bd0148e67'
client_secret='632854be9dbd4be18149ad249e855ff4'
redirect_uri='https://example.com/callback/'

scope = 'playlist-read-private'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists_dict = {}
username = None

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('username')
def handle_username(user_name):
    username = user_name
    playlists = sp.user_playlists(user_name)
    playlists_iter = playlists['items']
    for playlist in playlists_iter:
        name = playlist['name']
        emit('add-playlist', name)
        playlists_dict[name] = playlist

@socketio.on('execute')
def handle_execute(playlist_name):
    playlist = playlists_dict[playlist_name]
    playlist_data = get_data(sp, username, playlist)
    songs_to_csv(playlist_data, 'training.csv')
    artist_data = consolidate_df('training.csv')
    print('Getting related artist songs')
    related_artist_data = get_related_artists(sp, artist_data)
    songs_to_csv(related_artist_data, 'test.csv')
    recommended = find_top_10(sp, 'test.csv', 'training.csv', 5)
    for track in list(recommended.values()):
        #emit('add-recommendation', [track['name'], track['artists'][0]['name'], track['preview_url']])
        print('Name: {0} | Artist: {1}'.format(track['name'], track['artists'][0]['name']))


if __name__ == '__main__':
    socketio.run(app)
