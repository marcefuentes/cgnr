""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob
import sys

import pandas as pd

from common_modules.get_config import get_config
import modules_results.modes as mm


def get_columns(mode_is_trait, mode):
    """Get the columns for the given mode."""

    if mode_is_trait:
        columns = mm.dict_traits[mode]["variants"]
        return columns
    columns = mm.dict_multitrait_columns[mode]
    return columns


def get_data(mode_is_trait, mode, histogram, movie, clean):
    """Get the data for the given mode."""

    if mode_is_trait:
        return get_data_single_trait(mode, histogram, movie, clean)
    return get_data_multitrait(mode, histogram, movie, clean)


def get_data_multitrait(mode, histogram, movie, clean):
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
        dfs.append(get_df(path, csv0, movie, clean))
        if histogram:
            dffrqs.append(get_df(path, csv1, movie, clean))
    if "none" in rows:
        df_none = dfs[rows.index("none")]
    else:
        path = f"none/{mm.GIVEN_FOLDER}"
        df_none = get_df(path, csv0, movie, clean)
    if "social" in rows:
        df_social = dfs[rows.index("social")]
    else:
        path = "none/given000"
        df_social = get_df(path, csv0, movie, clean)

    return dfs, df_none, df_social, dffrqs, df_social


def get_data_single_trait(mode, histogram, movie, clean):
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
                get_df(
                    f"{prefix}_{suffix}/{mechanism}/{mm.GIVEN_FOLDER}",
                    csv0,
                    movie,
                    clean,
                )
                for prefix in variant_prefixes
            ]
        )
        df_nones.append(
            [
                get_df(f"{prefix}_{suffix}/none/{mm.GIVEN_FOLDER}", csv0, movie, clean)
                for prefix in variant_prefixes
            ]
        )
        df_socials.append(
            [
                get_df(f"{prefix}_{suffix}/none/given000", csv0, movie, clean)
                for prefix in variant_prefixes
            ]
        )
        if histogram:
            dffrqs.append(
                [
                    get_df(
                        f"{prefix}_{suffix}/{mechanism}/{mm.GIVEN_FOLDER}",
                        csv1,
                        movie,
                        clean,
                    )
                    for prefix in variant_prefixes
                ]
            )

    return dfs, df_nones, df_socials, dffrqs, df_socials[0][0]


def get_df(path, filetype, movie, clean):
    """Return a concatenated dataframe of the 'filetype' files in the given directory."""

    concatenated = os.path.join(path, f"concatenated{filetype}")

    if not movie and os.path.exists(concatenated):
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


def get_rows(mode_is_trait, mode):
    """Get the rows for the given mode."""

    if mode_is_trait:
        rows = mm.dict_single_trait_mechanisms.get(
            mode, mm.dict_single_trait_mechanisms["default"]
        )
        return rows
    rows = mm.dict_multitrait_rows.get(mode, mm.dict_multitrait_rows["default"])
    return rows


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
