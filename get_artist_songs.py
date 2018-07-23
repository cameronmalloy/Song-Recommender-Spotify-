from get_playlists import *

def get_related_artists(sp, artists):
    related_artists = []
    for artist in artists:
        related_artists.extend(sp.artist_related_artists(artist)['artists'][:3])
    print(len(related_artists))
    related_artists_ids = []
    for artist in related_artists:
        artist_id = artist['id']
        if not artist_id in related_artists_ids:
            related_artists_ids.append(artist['id'])
    print(related_artists_ids)
    print(len(related_artists_ids))
    #create songs dictionary from get_playlists file
    songs_data = setup_songs('uri', 'track_href')
    for i, ra_id in enumerate(related_artists_ids):
        print(i)
        albums = sp.artist_albums(ra_id)['items']
        get_album_songs(sp, albums, songs_data)
    return songs_data

def get_album_songs(sp, album_items, songs):
    previous_albums = []
    for album in album_items:
        if not album['name'] in previous_albums:
            previous_albums.append(album['name'])
            tracks = sp.album_tracks(album['id'])['items']
            #tracks = sp.album_tracks(album['id'])
            #tracks = tracks['items']
            track_lst = []
            for track in tracks:
                track_lst.append(track['id'])
            audio_features = sp.audio_features(track_lst)
            for features in audio_features:
                if features:
                    songs['uri'] = np.append(songs['uri'], features['uri'])
                    songs['track_href'] = np.append(songs['track_href'], features['track_href'])
                    for feature in all_features:
                        songs[feature] = np.append(songs[feature], features.get(feature, np.nan))
            '''
            for track in tracks:
                features = sp.audio_features(track['id'])[0]
                if features:
                    songs['name'] = np.append(songs['name'], track['name'])
                    songs['artist_id'] = np.append(songs['artist_id'], track['artists'][0]['id'])
                    songs['song_id'] = np.append(songs['song_id'], track['id'])
                    for feature in all_features:
                        #update song features
                        songs[feature] = np.append(songs[feature], features.get(feature, np.nan))
                        '''
