""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob
import sys

import numpy as np
import pandas as pd


def get_dynamic_data(data_layout, options, csv, frq):
    """Get the df args for the given trait_set."""

    nrows = len(data_layout["variants"])
    ncols = len(data_layout["variants"][0])

    dynamic_data = {
        "dfs": np.empty((nrows, ncols), dtype=object),
        "dfs_control": np.empty((nrows, ncols), dtype=object),
    }

    for i in range(nrows):
        for j in range(ncols):
            path = f"{data_layout['variants'][i][j]}/{data_layout['mechanisms'][i][j]}/{data_layout['givens'][i][j]}"
            dynamic_data["dfs"][i][j] = get_df(
                path, csv, options["movie"], options["clean"]
            )
            if data_layout["mechanisms_control"][i][j] not in ["", "None"]:
                path = f"{data_layout['variants_control'][i][j]}/{data_layout['mechanisms_control'][i][j]}/{data_layout['givens_control'][i][j]}"
                dynamic_data["dfs_control"][i][j] = get_df(
                    path, csv, options["movie"], options["clean"]
                )

    if options["histogram"]:
        dynamic_data["dffrqs"] = np.empty((nrows, ncols), dtype=object)
        for i in range(nrows):
            for j in range(ncols):
                dynamic_data["dffrqs"][i][j] = get_df(
                    path, frq, options["movie"], options["clean"]
                )

    df = dynamic_data["dfs"][0, 0]

    dynamic_data["frames"] = df.Time.unique()
    dynamic_data["alphas"] = np.sort(df["alpha"].unique())[::-1]
    dynamic_data["logess"] = np.sort(df["logES"].unique())
    if options["fitness"]:
        dynamic_data["rhos"] = 1.0 - 1.0 / np.power(2.0, dynamic_data["logess"])

    return dynamic_data


def get_df(path, filetype, movie, clean):
    """Return a concatenated dataframe of the 'filetype' files in the given directory."""

    if not os.path.exists(path):
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
        print(f"No {path}/*{filetype} files found.")
        sys.exit()
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
