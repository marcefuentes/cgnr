""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import numpy as np
from resultsm.get_df import get_df


def get_data(layout, options, csv, frq):
    """Get the df args for the given trait_set."""

    nrows = len(layout["variants"])
    ncols = len(layout["variants"][0])

    data = {
        "dfs": np.empty((nrows, ncols), dtype=object),
        "dfs_control": np.empty((nrows, ncols), dtype=object),
        "traits": layout["traits"],
    }

    params = {
        "path": "",
        "filetype": csv,
        "movie": options["movie"],
        "clean": options["clean"],
    }

    df = None

    for i in range(nrows):
        for j in range(ncols):
            params["path"] = (
                f"{layout['variants'][i][j]}/"
                f"{layout['mechanisms'][i][j]}/"
                f"{layout['givens'][i][j]}"
            )
            data["dfs"][i][j] = get_df(**params)
            if not data["dfs"][i][j].empty:
                df = data["dfs"][i][j]
            if layout["mechanisms_control"][i][j] not in ["", "None"]:
                params["path"] = (
                    f"{layout['variants_control'][i][j]}/"
                    f"{layout['mechanisms_control'][i][j]}/"
                    f"{layout['givens_control'][i][j]}"
                )
                data["dfs_control"][i][j] = get_df(**params)

    if df is None:
        raise ValueError("No data found in any of the paths defined in layout.")

    if options["histogram"]:
        data["dffrqs"] = np.empty((nrows, ncols), dtype=object)
        params["filetype"] = frq
        for i in range(nrows):
            for j in range(ncols):
                params["path"] = (
                    f"{layout['variants'][i][j]}/"
                    f"{layout['mechanisms'][i][j]}/"
                    f"{layout['givens'][i][j]}"
                )
                data["dffrqs"][i][j] = get_df(**params)

    data["frames"] = df.Time.unique()
    data["alphas"] = np.sort(df["alpha"].unique())[::-1]
    data["logess"] = np.sort(df["logES"].unique())
    if options["layout"] == "curves" or options["layout"] == "theory":
        data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    return data
