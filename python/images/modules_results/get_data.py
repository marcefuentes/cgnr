""" This module reads the csv files in the given directory and returns a concatenated dataframe. """

import os
from glob import glob
import sys

import numpy as np
import pandas as pd

from settings_results.data_constants import data_constants
import settings_results.layouts_single_folder as s_folder
import settings_results.layouts_single_trait as s_trait
from settings_project.project import project


def get_columns(single_trait, trait_set, single_folder):
    """Get the columns for the given trait_set."""

    if single_trait and single_folder:
        columns = [""]
        return columns
    if single_trait:
        columns = s_trait.columns
        return columns
    columns = s_folder.columns[trait_set]
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


def get_df_single_folder(trait_set, histogram, movie, clean):
    """Get the df for several traits in a variant."""

    csv0, csv1 = project["output_file_extensions"]

    rows = s_folder.rows.get(trait_set, s_folder.rows["default"])

    dfs, dffrqs = [], []

    given_folder = data_constants["given_folder"]

    for row in rows:
        if row == "social":
            path = "none/0.0"
        elif "none" in row:
            path = f"none/{given_folder}"
        elif "none" in trait_set:
            path = f"none/{row}"
        else:
            path = f"{row}/{given_folder}"
        dfs.append(get_df(path, csv0, movie, clean))
        if histogram:
            dffrqs.append(get_df(path, csv1, movie, clean))
    if "none" in rows:
        df_none = dfs[rows.index("none")]
    else:
        path = f"none/{given_folder}"
        df_none = get_df(path, csv0, movie, clean)
    if "social" in rows:
        df_social = dfs[rows.index("social")]
    else:
        path = "none/0.0"
        df_social = get_df(path, csv0, movie, clean)

    return dfs, df_none, df_social, dffrqs, df_social


def get_df_single_trait(histogram, movie, clean):
    """Get the df for a trait across several variants."""

    csv0, csv1 = project["output_file_extensions"]

    dfs, dffrqs, df_nones, df_socials = [], [], [], []

    given_folder = data_constants["given_folder"]
    for suffix, row in zip(s_trait.variant_suffixes, s_trait.rows):
        dfs.append(
            [
                get_df(
                    f"{column}_{suffix}/{row}/{given_folder}",
                    csv0,
                    movie,
                    clean,
                )
                for column in s_trait.columns
            ]
        )
        if histogram:
            dffrqs.append(
                [
                    get_df(
                        f"{column}_{suffix}/{row}/{given_folder}",
                        csv1,
                        movie,
                        clean,
                    )
                    for column in s_trait.columns
                ]
            )
        df_nones.append(
            [
                get_df(f"{column}_{suffix}/none/{given_folder}", csv0, movie, clean)
                for column in s_trait.columns
            ]
        )
        df_socials.append(
            [
                get_df(f"{column}_{suffix}/none/0.0", csv0, movie, clean)
                for column in s_trait.columns
            ]
        )

    return dfs, df_nones, df_socials, dffrqs, df_socials[0][0]


def get_df_single_trait_single_folder(histogram, movie, clean):
    """Get the df for a trait across several variants."""

    csv0, csv1 = project["output_file_extensions"]
    given_folder = os.path.basename(os.getcwd())

    df, dffrq, df_none, df_social = [[]], [[]], [[]], [[]]
    df[0].append(get_df(".", csv0, movie, clean))
    if histogram:
        dffrq[0].append(get_df(".", csv1, movie, clean))
    df_none[0].append(get_df(f"../../none/{given_folder}", csv0, movie, clean))
    df_social[0].append(get_df("../../none/0.0", csv0, movie, clean))

    return df, df_none, df_social, dffrq, df_social[0][0]


def get_rows(single_trait, trait_set, single_folder):
    """Get the rows for the given trait_set."""

    if single_trait and single_folder:
        return [""]
    if single_trait:
        return s_trait.rows
    return s_folder.rows.get(trait_set, s_folder.rows["default"])


def get_data(data_dict, clean):
    """Get the df args for the given trait_set."""

    if data_dict["single_trait"] and data_dict["single_folder"]:
        (
            data_dict["dfs"],
            data_dict["df_none"],
            data_dict["df_social"],
            data_dict["dffrqs"],
            df,
        ) = get_df_single_trait_single_folder(
            data_dict["histogram"],
            data_dict["movie"],
            clean,
        )

    elif data_dict["single_trait"]:
        (
            data_dict["dfs"],
            data_dict["df_none"],
            data_dict["df_social"],
            data_dict["dffrqs"],
            df,
        ) = get_df_single_trait(
            data_dict["histogram"],
            data_dict["movie"],
            clean,
        )
    else:
        (
            data_dict["dfs"],
            data_dict["df_none"],
            data_dict["df_social"],
            data_dict["dffrqs"],
            df,
        ) = get_df_single_folder(
            data_dict["trait_set"],
            data_dict["histogram"],
            data_dict["movie"],
            clean,
        )

    data_dict["frames"] = df.Time.unique()
    data_dict["alphas"] = np.sort(df["alpha"].unique())[::-1]
    data_dict["logess"] = np.sort(df["logES"].unique())
    if data_dict["fitness"]:
        data_dict["rhos"] = 1.0 - 1.0 / np.power(2.0, data_dict["logess"])

    return data_dict


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
