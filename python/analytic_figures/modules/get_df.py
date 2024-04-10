
""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob
import pandas as pd

def read_files(filelist, movie):
    """ Read the csv files in the given directory and return a concatenated dataframe. """
    df_list = [None] * len(filelist)
    for i, file in enumerate(filelist):
        df = pd.read_csv(file)
        if not movie:
            df = df.tail(1)
        df_list[i] = df
    dfc = pd.concat(df_list, ignore_index=True)
    return dfc

def get_df(row, filetype, movie):
    """ Return a concatenated dataframe of the csv files in the given directory. """
    if row == "social":
        row = "none/given000"
    elif "none" in row:
        row = "none/given100"
    else:
        row = f"{row}/given100"
    filelist = glob(os.path.join(row, f"*.{filetype}"))
    if not filelist:
        print(f"No {row}/*.{filetype} files found.")
        exit()
    df = read_files(filelist, movie)
    return df
