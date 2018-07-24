import numpy as np
import pandas as pd

def normalize_df(df):
    columns = list(df.columns.values)
    columns.pop(0)
    columns.pop(0)
    for col in columns:
        c_min = np.min(df[col])
        c_max = np.max(df[col])
        df[col] = (df[col] - c_min) / (c_max - c_min)

def find_dist(row1, row2):
    for _ in range(3):
        row1.pop(0)
        row2.pop(0)
    row1 = np.array(row1)
    row2 = np.array(row2)
    return np.sum((row1 - row2) ** 2) ** .5

def delete_furthest_distance(curr_row, df):
    distances = []
    for i in range(len(df.iloc[:,0:1])):#range(curr_row + 1, len(df.iloc[:,0:1])):
        row1 = list(df.iloc[curr_row].values)
        row2 = list(df.iloc[i].values)
        distances.append(find_dist(row1, row2))
    df.drop(distances.index(max(distances)), inplace=True)

def find_num_rows(df):
    return len(df.iloc[:,0:1])

def ten_percent_rows(df):
    num_rows = find_num_rows(df)
    if num_rows < 10:
        return
    ten_percent = np.ceil(num_rows * .1)
    if ten_percent < 10:
        ten_percent = 10
    curr_row = 0
    while find_num_rows(df) > ten_percent:
        delete_furthest_distance(curr_row, df)
        df.reset_index(inplace=True, drop=True)
        curr_row = (curr_row + 1) % len(df.iloc[:,0:1])

def consolidate_df(file_name):
    df = pd.read_csv(file_name)
    normalize_df(df)
    ten_percent_rows(df)
    return df['artist_id'].values
