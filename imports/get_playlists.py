import numpy as np
'''Gets the playlists for a certain user'''

def show_tracks(tracks):
    ''' Prints out the tracks in the following format:
        <#> <Artist Name> <Track Name>'''
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print('{0} {1} {2}'.format(i, track['artists'][0]['name'], track['name']))
        #print('{0} {1} {2}'.format(i, track['artists'][0].keys(), track['name']))

def get_all_playlists(sp, username):
    ''' Returns all the playlists the user has created '''
    playlists = sp.user_playlists(username)
    ret_playlists = []
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            ret_playlists.append(playlist)
    return ret_playlists

#establishes all the features of songs
all_features = ['danceability', 'duration_ms', 'energy', 'key', 'loudness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

def setup_songs(name1, name2):
    ''' Create a dictionary with of name + all_features as keys. Values are empty numpy arrays '''
    ret_dict = {}
    ret_dict[name1] = np.array([])
    ret_dict[name2] = np.array([])
    for feature in all_features:
        ret_dict[feature] = np.array([])
    return ret_dict

def get_data(sp, username, playlist):
    ''' Extracts all tracks of a playlist and grabs the features and returns a dictionary.
        Keys: name + elements in all_features
        Values: name + all the features for every song in the playlist '''
    print()
    print(playlist['name'])
    print(' total tracks', playlist['tracks']['total'])
    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
    tracks = results['tracks']
    #Setup artist data
    #artist_data = []
    #Setup dictionary for DataFrame
    songs_data = setup_songs('artist_id', 'song_id')
    get_tracks_and_features(sp, tracks, songs_data)
    while tracks['next']:
        tracks = sp.next(tracks)
        get_tracks_and_features(sp, tracks, songs_data)
    return songs_data

def get_tracks_and_features(sp, tracks, songs):
    for item in tracks['items']:
        track = item['track']
        #update artists id's
        #artists.append(track['artists'][0]['id'])
        #update song name's
        features = sp.audio_features(track['id'])[0]
        if features:
            songs['artist_id'] = np.append(songs['artist_id'], track['artists'][0]['id'])
            songs['song_id'] = np.append(songs['song_id'], track['id'])
            for feature in all_features:
                #update song features
                songs[feature] = np.append(songs[feature], features.get(feature, np.nan))
