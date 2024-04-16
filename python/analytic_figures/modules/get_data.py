""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob
import pandas as pd

from common_modules.get_config import get_config
import modules.modes as mm


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


def get_df(path, filetype, movie):
    """Return a concatenated dataframe of the csv files in the given directory."""

    filelist = glob(os.path.join(path, f"*{filetype}"))
    if not filelist:
        print(f"No {path}/*{filetype} files found.")
        exit()
    df = read_files(filelist, movie)
    return df


def get_data_multitrait(mode, histogram, movie):
    """Get the data for several traits in a variant."""

    csv0, csv1 = get_config("output_file_extensions")

    rows = mm.dict_multitrait_rows.get(mode, mm.dict_multitrait_rows["default"])

    dfs = []
    dffrqs = []

    for row in rows:
        if row == "social":
            path = "none/given000"
        elif "none" in row:
            path = f"none/{mm.GIVEN_FOLDER}"
        elif "none" in mode:
            path = f"none/{row}"
        else:
            path = f"{row}/{mm.GIVEN_FOLDER}"
        dfs.append(get_df(path, csv0, movie))
        if histogram:
            dffrqs.append(get_df(path, csv1, movie))
    if "none" in rows:
        df_none = dfs[rows.index("none")]
    else:
        path = f"none/{mm.GIVEN_FOLDER}"
        df_none = get_df(path, csv0, movie)
    if "social" in rows:
        df_social = dfs[rows.index("social")]
    else:
        path = "none/given000"
        df_social = get_df(path, csv0, movie)
    return dfs, df_none, df_social, dffrqs


def get_data_single_trait(mode, histogram, movie):
    """Get the data for a trait across several variants."""

    csv0, csv1 = get_config("output_file_extensions")

    columns = mm.dict_traits[mode]["variants"]
    rows_0 = mm.dict_single_trait_rows_0.get(
        mode, mm.dict_single_trait_rows_0["default"]
    )
    rows_1 = mm.dict_single_trait_rows_1.get(
        mode, mm.dict_single_trait_rows_1["default"]
    )

    nrows = len(rows_0)
    ncolumns = len(columns)

    dfs = [[None for _ in range(ncolumns)] for _ in range(nrows)]
    df_nones = [[None for _ in range(ncolumns)] for _ in range(nrows)]
    df_socials = [[None for _ in range(ncolumns)] for _ in range(nrows)]
    if histogram:
        dffrqs = [[None for _ in range(ncolumns)] for _ in range(nrows)]
    else:
        dffrqs = []

    for r, row_0, row_1 in zip(range(nrows), rows_0, rows_1):
        for c, column in enumerate(columns):
            path = f"{column}_{row_0}/{row_1}/{mm.GIVEN_FOLDER}"
            none_path = f"{column}_{row_0}/none/{mm.GIVEN_FOLDER}"
            social_path = f"{column}_{row_0}/none/given000"
            if histogram:
                dffrqs[r][c] = get_df(path, csv1, movie)
            dfs[r][c] = get_df(path, csv0, movie)
            df_nones[r][c] = get_df(none_path, csv0, movie)
            df_socials[r][c] = get_df(social_path, csv0, movie)

    return dfs, df_nones, df_socials, dffrqs
