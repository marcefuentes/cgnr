""" Reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob

import pandas as pd


def get_df(path, filetype, clean, movie):
    """Return a concatenated dataframe of the 'filetype' files in the given directory."""

    if not os.path.exists(path):
        print(f"{path} does not exist.")
        return pd.DataFrame()

    if movie:
        concatenated = os.path.join(path, f"{filetype[1:]}_for_movie.con")
    else:
        concatenated = os.path.join(path, f"{filetype[1:]}_for_image.con")

    if os.path.exists(concatenated):
        if clean:
            os.remove(concatenated)
        else:
            df = pd.read_csv(concatenated)
            return df

    filelist = glob(os.path.join(path, f"*{filetype}"))
    if not filelist:
        print(f"\nNo {path}/*{filetype} files found.")
        return pd.DataFrame()
    df = read_files(filelist, movie)

    df.to_csv(concatenated, index=False)

    return df


def read_files(filelist, movie):
    """Read the csv files in the given directory and return a concatenated dataframe."""

    df_list = [None] * len(filelist)
    for i, file in enumerate(filelist):
        df = pd.read_csv(file)
        if not movie:
            df = df.tail(1)
        df_list[i] = df
    dfc = pd.concat(df_list, ignore_index=True)
    return dfc
