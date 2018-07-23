import numpy as np
import pandas as pd

def songs_to_csv(songs, file_name):
    df = pd.DataFrame(songs)
    df.to_csv(file_name, index=False)
