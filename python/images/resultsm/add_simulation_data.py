"""Add dataframes from csv files to data."""

import numpy as np
from resultsm.get_df import get_df
from settings.project import project


def add_simulation_data(data):
    """Add dataframes from csv files to data."""

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
