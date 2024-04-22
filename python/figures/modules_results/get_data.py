""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob
import sys

import pandas as pd

from common_modules.get_config import get_config
import modules_results.modes as mm


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

    variant_prefixes = mm.dict_traits[mode]["variants"]
    variant_suffixes = mm.dict_single_trait_variant_suffixes.get(
        mode, mm.dict_single_trait_variant_suffixes["default"]
    )
    mechanisms = mm.dict_single_trait_mechanisms.get(
        mode, mm.dict_single_trait_mechanisms["default"]
    )

    dfs = []
    df_nones = []
    df_socials = []
    dffrqs = []

    for suffix, mechanism in zip(variant_suffixes, mechanisms):
        dfs.append(
            [
                get_df(f"{prefix}_{suffix}/{mechanism}/{mm.GIVEN_FOLDER}", csv0, movie)
                for prefix in variant_prefixes
            ]
        )
        df_nones.append(
            [
                get_df(f"{prefix}_{suffix}/none/{mm.GIVEN_FOLDER}", csv0, movie)
                for prefix in variant_prefixes
            ]
        )
        df_socials.append(
            [
                get_df(f"{prefix}_{suffix}/none/given000", csv0, movie)
                for prefix in variant_prefixes
            ]
        )
        if histogram:
            dffrqs.append(
                [
                    get_df(
                        f"{prefix}_{suffix}/{mechanism}/{mm.GIVEN_FOLDER}", csv1, movie
                    )
                    for prefix in variant_prefixes
                ]
            )

    return dfs, df_nones, df_socials, dffrqs


def get_df(path, filetype, movie):
    """Return a concatenated dataframe of the csv files in the given directory."""

    filelist = glob(os.path.join(path, f"*{filetype}"))
    if not filelist:
        print(f"No {path}/*{filetype} files found.")
        sys.exit()
    df = read_files(filelist, movie)
    return df


def get_rows_columns(mode, mode_is_trait):
    """Get the rows and columns for the given mode."""

    column_titles = []
    row_titles = []

    if mode_is_trait:
        rows = mm.dict_single_trait_mechanisms.get(
            mode, mm.dict_single_trait_mechanisms["default"]
        )
        columns = mm.dict_traits[mode]["variants"]
        for column in columns:
            column_titles.append(mm.dict_variant_titles[column])
    else:
        rows = mm.dict_multitrait_rows.get(mode, mm.dict_multitrait_rows["default"])
        columns = mm.dict_multitrait_columns[mode]
        for column in columns:
            column_titles.append(mm.dict_traits[column]["title"])
    for row in rows:
        row_titles.append(mm.dict_row_titles[row])

    return rows, row_titles, columns, column_titles


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
