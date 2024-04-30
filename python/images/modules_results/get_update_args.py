""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob
import sys

import numpy as np
import pandas as pd

from common_modules.get_config import get_config
from modules.get_setting import get_setting
from modules.theory import fitness
import modules_results.trait_sets_config as mm


def get_columns(single_trait, trait_set, single_folder):
    """Get the columns for the given trait_set."""

    if single_trait and single_folder:
        columns = [""]
        return columns
    if single_trait:
        columns = mm.dict_traits[trait_set]["variants"]
        return columns
    columns = mm.dict_multitrait_columns[trait_set]
    return columns


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


def get_df_multitrait(trait_set, curve, movie, clean):
    """Get the df for several traits in a variant."""

    csv0, csv1 = get_config("output_file_extensions")

    rows = mm.dict_multitrait_rows.get(trait_set, mm.dict_multitrait_rows["default"])

    dfs, dffrqs = [], []

    for row in rows:
        if row == "social":
            path = "none/given000"
        elif "none" in row:
            path = f"none/{mm.GIVEN_FOLDER}"
        elif "none" in trait_set:
            path = f"none/{row}"
        else:
            path = f"{row}/{mm.GIVEN_FOLDER}"
        dfs.append(get_df(path, csv0, movie, clean))
        if curve == "histogram":
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


def get_df_single_trait(trait_set, curve, movie, clean):
    """Get the df for a trait across several variants."""

    csv0, csv1 = get_config("output_file_extensions")

    variant_prefixes = mm.dict_traits[trait_set]["variants"]
    variant_suffixes = mm.dict_single_trait_variant_suffixes.get(
        trait_set, mm.dict_single_trait_variant_suffixes["default"]
    )
    mechanisms = mm.dict_single_trait_mechanisms.get(
        trait_set, mm.dict_single_trait_mechanisms["default"]
    )

    dfs, dffrqs, df_nones, df_socials = [], [], [], []

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
        if curve == "histogram":
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

    return dfs, df_nones, df_socials, dffrqs, df_socials[0][0]


def get_df_single_trait_single_folder(trait_set, curve, movie, clean):
    """Get the df for a trait across several variants."""

    csv0, csv1 = get_config("output_file_extensions")
    given_folder = os.path.basename(os.getcwd())

    dffrq = pd.DataFrame()

    df = get_df(".", csv0, movie, clean)
    if curve == "histogram":
        dffrq = get_df(".", csv1, movie, clean)
    df_none = get_df(f"../../none/{given_folder}", csv0, movie, clean)
    df_social = get_df("../../none/given000", csv0, movie, clean)

    return df, df_none, df_social, dffrq, df_social


def get_rows(single_trait, trait_set, single_folder):
    """Get the rows for the given trait_set."""

    if single_trait and single_folder:
        rows = [""]
        return rows
    if single_trait:
        rows = mm.dict_single_trait_mechanisms.get(
            trait_set, mm.dict_single_trait_mechanisms["default"]
        )
        return rows
    rows = mm.dict_multitrait_rows.get(trait_set, mm.dict_multitrait_rows["default"])
    return rows


def get_update_args(update_args, clean):
    """Get the df args for the given trait_set."""

    if update_args["curve"] == "landscape":
        update_args["n_x_values"] = get_setting(update_args["file_name"], "n_x_values")
    elif update_args["curve"] == "histogram":
        update_args["n_x_values"] = get_config("bins")

    if update_args["single_trait"] and update_args["single_folder"]:
        function = get_df_single_trait_single_folder
    elif update_args["single_trait"]:
        function = get_df_single_trait
    else:
        function = get_df_multitrait

    (
        update_args["dfs"],
        update_args["df_none"],
        update_args["df_social"],
        update_args["dffrqs"],
        df,
    ) = function(update_args["trait_set"], update_args["curve"], update_args["movie"], clean)

    update_args["frames"] = df.Time.unique()
    update_args["alphas"] = np.sort(df["alpha"].unique())[::-1]
    update_args["logess"] = np.sort(df["logES"].unique())

    return update_args


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
