""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import numpy as np
from modules_results.get_df import get_df


def get_dynamic_data(data_layout, options, csv, frq):
    """Get the df args for the given trait_set."""

    nrows = len(data_layout["variants"])
    ncols = len(data_layout["variants"][0])

    dynamic_data = {
        "dfs": np.empty((nrows, ncols), dtype=object),
        "dfs_control": np.empty((nrows, ncols), dtype=object),
        "traits": data_layout["traits"],
    }

    params = {
        "path": "",
        "filetype": csv,
        "movie": options["movie"],
        "clean": options["clean"],
    }

    for i in range(nrows):
        for j in range(ncols):
            params["path"] = f"{data_layout['variants'][i][j]}/{data_layout['mechanisms'][i][j]}/{data_layout['givens'][i][j]}"
            dynamic_data["dfs"][i][j] = get_df(**params)
            if data_layout["mechanisms_control"][i][j] not in ["", "None"]:
                params["path"] = f"{data_layout['variants_control'][i][j]}/{data_layout['mechanisms_control'][i][j]}/{data_layout['givens_control'][i][j]}"
                dynamic_data["dfs_control"][i][j] = get_df(**params)

    if options["histogram"]:
        dynamic_data["dffrqs"] = np.empty((nrows, ncols), dtype=object)
        params["filetype"] = frq
        for i in range(nrows):
            for j in range(ncols):
                params["path"] = f"{data_layout['variants'][i][j]}/{data_layout['mechanisms'][i][j]}/{data_layout['givens'][i][j]}"
                dynamic_data["dffrqs"][i][j] = get_df(**params)

    df = dynamic_data["dfs"][0, 0]

    dynamic_data["frames"] = df.Time.unique()
    dynamic_data["alphas"] = np.sort(df["alpha"].unique())[::-1]
    dynamic_data["logess"] = np.sort(df["logES"].unique())
    if options["figure"] == "curves":
        dynamic_data["rhos"] = 1.0 - 1.0 / np.power(2.0, dynamic_data["logess"])

    return dynamic_data
