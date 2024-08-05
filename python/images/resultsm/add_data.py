""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import numpy as np

from resultsm.get_df import get_df
from resultsm.get_static_data import get_static_data

from settings.project import project


def add_data(data, image):
    """Get the df args for the given trait_set."""

    layout = (data["layout_i"], data["layout_j"])
    rows = range(layout[0])
    cols = range(layout[1])

    data["column_index"] = "logES"
    data["row_index"] = "alpha"

    data["dfs"] = np.empty(layout, dtype=object)
    data["dfs_control"] = np.empty(layout, dtype=object)

    csv, frq = project["output_file_extensions"]
    params = {
        "path": "",
        "filetype": csv,
        "movie": data["movie"],
        "clean": data["clean"],
    }

    df = None

    for i in rows:
        for j in cols:
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
        data["dffrqs"] = np.empty(layout, dtype=object)
        params["filetype"] = frq
        for i in rows:
            for j in cols:
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
    image["nr"] = data["layout_k"] = len(data["alphas"])
    image["nc"] = data["layout_m"] = len(data["rhos"])
    image["fig_layout"] = {
        "nc": (1 if data["ax_type"] == "AxesImage" else image["nc"]),
        "ncols": data["layout_j"],
        "nr": (1 if data["ax_type"] == "AxesImage" else image["nr"]),
        "nrows": data["layout_i"],
    }
    image["letters"]["y"] = 1.0 + image["padding_letter"] * image["fig_layout"]["nr"]
    image["titles_columns"] = data["titles_columns"]
    image["titles_rows"] = data["titles_rows"]
    image["ticklabels_x"] = [
        f"{data["rhos"][0]:.0f}",
        f"{data["rhos"][data['layout_m'] // 2]:.0f}",
        f"{data["rhos"][-1]:.2f}",
    ]
    image["ticklabels_y"] = [
        f"{data["alphas"][0]:.1f}",
        f"{data["alphas"][data['layout_k'] // 2]:.1f}",
        f"{data["alphas"][-1]:.1f}",
    ]

    if data["layout"] == "curves":
        data["x"], data["y"] = get_static_data(
            data["traits"],
            data["givens"],
            data["alphas"],
            data["rhos"],
        )
        image["lim_x"] = [0, 1]
        image["lim_y"] = [0, 1]
        image["margin_top"] *= 0.5
    elif data["histogram"]:
        data["x"] = np.arange(project["bins"])
        data["y"] = np.zeros_like(data["x"])
        image["lim_x"] = [-2, len(data["x"]) + 1]
        image["lim_y"] = [0, 0.25]
    else:
        data["x"] = None
        data["y"] = np.zeros((data["layout_k"], data["layout_m"]))
        image["lim_x"] = [None, None]
        image["lim_y"] = [None, None]
