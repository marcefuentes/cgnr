""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import numpy as np

from resultsm.get_df import get_df
from resultsm.get_static_data import get_static_data
from resultsm.get_theory_axesimage import get_theory_axesimage

from settings.project import project


def get_data(data):
    """Get the df args for the given trait_set."""

    nrows = len(data["variants"])
    ncols = len(data["variants"][0])

    data["dfs"] = np.empty((nrows, ncols), dtype=object)
    data["dfs_control"] = np.empty((nrows, ncols), dtype=object)

    csv, frq = project["output_file_extensions"]
    params = {
        "path": "",
        "filetype": csv,
        "movie": data["movie"],
        "clean": data["clean"],
    }

    df = None

    for i in range(nrows):
        for j in range(ncols):
            params["path"] = (
                f"{data['variants'][i][j]}/"
                f"{data['mechanisms'][i][j]}/"
                f"{data['givens'][i][j]}"
            )
            data["dfs"][i][j] = get_df(**params)
            if not data["dfs"][i][j].empty:
                df = data["dfs"][i][j]
            if data["mechanisms_control"][i][j] not in ["", "None"]:
                params["path"] = (
                    f"{data['variants_control'][i][j]}/"
                    f"{data['mechanisms_control'][i][j]}/"
                    f"{data['givens_control'][i][j]}"
                )
                data["dfs_control"][i][j] = get_df(**params)

    if df is None:
        raise ValueError("No data found in any of the paths defined in data.")

    if data["histogram"]:
        data["dffrqs"] = np.empty((nrows, ncols), dtype=object)
        params["filetype"] = frq
        for i in range(nrows):
            for j in range(ncols):
                params["path"] = (
                    f"{data['variants'][i][j]}/"
                    f"{data['mechanisms'][i][j]}/"
                    f"{data['givens'][i][j]}"
                )
                data["dffrqs"][i][j] = get_df(**params)

    data["frames"] = df.Time.unique()
    data["alphas"] = np.sort(df["alpha"].unique())[::-1]
    data["logess"] = np.sort(df["logES"].unique())
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])
    if data["layout"] == "curves":
        data["x"], data["y"] = get_static_data(
            data["traits"],
            data["givens"],
            data["alphas"],
            data["rhos"],
        )
    elif data["histogram"]:
        data["x"] = np.arange(project["bins"])
        data["y"] = np.zeros(
            (nrows, ncols, len(data["alphas"]), len(data["rhos"]), project["bins"])
        )
    elif data["layout"] == "theory":
        data["x"], data["y"] = get_theory_axesimage(
            data["traits"], data["givens"], data["alphas"], data["rhos"]
        )
    else:
        data["x"] = None
        data["y"] = np.zeros(
            (nrows, ncols, 1, 1, len(data["alphas"]), len(data["rhos"]))
        )
