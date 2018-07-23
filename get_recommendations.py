import numpy as np
import pandas as pd

from consolidated_playlist_artists import *

def reduce_tempo(df):
    df['tempo'] = df['tempo'] * .95

def find_dist_new(row1, row2):
    row1 = list(row1)
    row2 = list(row2)
    for _ in range(2):
        row1.pop(0)
        row2.pop(0)
    row1 = np.array(row1)
    row2 = np.array(row2)
    return np.sum((row1 - row2) ** 2) ** .5

def find_closest_k(row, df, k):
    distances = list(df.apply(lambda df_row: find_dist_new(row, df_row), axis=1))
    distances.sort()
    return sum(distances[:k])

def find_top_10(sp, test_name, train_name, k):
    test_df = pd.read_csv(test_name)
    train_df = pd.read_csv(train_name)
    test_df['closeness'] = test_df.apply(lambda row: find_closest_k(row, train_df, k), axis=1)
    test_df.sort_values('closeness', inplace=True)
    test_df.reset_index(drop=True, inplace=True)

    tracks = list(test_df['uri'].values)
    recommended_tracks = {}
    i = 0
    while len(recommended_tracks) < 20:
        track_all = sp.track(tracks[i])
        if not track_all['name'] in recommended_tracks.keys():
            recommended_tracks[track_all['name']] = track_all
        i += 1
    return recommended_tracks
