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
                path = f"{data_layout['variants'][i][j]}/{data_layout['mechanisms'][i][j]}/{data_layout['givens'][i][j]}"
                dynamic_data["dffrqs"][i][j] = get_df(
                    path, frq, options["movie"], options["clean"]
                )

    df = dynamic_data["dfs"][0, 0]

    dynamic_data["frames"] = df.Time.unique()
    dynamic_data["alphas"] = np.sort(df["alpha"].unique())[::-1]
    dynamic_data["logess"] = np.sort(df["logES"].unique())
    if options["figure"] == "curves":
        dynamic_data["rhos"] = 1.0 - 1.0 / np.power(2.0, dynamic_data["logess"])

    return dynamic_data
