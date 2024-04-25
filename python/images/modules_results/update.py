""" Update data in artists. """

import re
import sys

import numpy as np
import pandas as pd

from matplotlib import colormaps

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get
import modules_results.modes as mm


def get_zmatrix(t, df, trait):
    """Returns the zmatrix for a given time, dataframe, and trait."""

    if trait not in df.columns:
        print(f"Trait {trait} not in the dataframe.")
        return None
    m = df.Time == t
    zmatrix = pd.pivot(df.loc[m], values=trait, index="alpha", columns="logES")
    zmatrix = zmatrix.sort_index(axis=0, ascending=False)
    zmatrix = zmatrix.to_numpy()
    return zmatrix


def update_artists(t, update_args):
    """Update the plot with the data at time t."""

    if update_args["movie"]:
        update_args["text"].set_text(t)

    for r, _ in enumerate(update_args["rows"]):
        for c, _ in enumerate(update_args["columns"]):
            zmatrix = update_zmatrix(t, update_args, r, c)
            if update_args["dffrqs"]:
                update_args["artists"][r, c] = update_histogram(
                    t, update_args, zmatrix, r, c
                )
            else:
                update_args["artists"][r, c].set_array(zmatrix)

    return update_args["artists"].flatten()


def update_histogram(t, update_args, zmatrix, r, c):
    """Update the histogram with the data at time t."""

    if update_args["mode_is_trait"]:
        df = update_args["dffrqs"][r][c]
        trait = mm.dict_traits[update_args["mode"]]["frq"]
    else:
        df = update_args["dffrqs"][r]
        trait = mm.dict_traits[update_args["columns"][0]]["frq"]

    for a, alpha in enumerate(update_args["alphas"]):
        for e, loges in enumerate(update_args["logess"]):
            d = df[(df["Time"] == t) & (df["alpha"] == alpha) & (df["logES"] == loges)]
            freq_a = [col for col in d.columns if re.match(rf"^{trait}\d+$", col)]
            y = d.loc[:, freq_a].values[0].flatten()
            update_args["artists"][r, c, a, e].set_ydata(y)
            bgcolor = colormaps[get("COMMON", "color_map")]((zmatrix[a, e] + 1) / 2)
            update_args["artists"][r, c, a, e].axes.set_facecolor(bgcolor)

    return update_args["artists"][r, c]


def update_zmatrix(t, update_args, r, c):
    """Return the updated zmatrix for a given time and trait."""

    if update_args["mode_is_trait"]:
        trait_in = update_args["mode"]
        df = update_args["dfs"][r][c]
        df_none = update_args["df_none"][r][c]
        df_social = update_args["df_social"][r][c]
    else:
        trait_in = update_args["columns"][c]
        df_none = update_args["df_none"]
        df_social = update_args["df_social"]
        df = update_args["dfs"][r]

    none = bool(update_args["rows"][r] == "none" and update_args["mode"] != "none")

    if "nothing" in trait_in:
        zmatrix = np.zeros((len(update_args["alphas"]), len(update_args["logess"])))
        return zmatrix

    if trait_in not in mm.dict_traits:
        print(f"Trait {trait_in} not in dictionary modes.py/dict_traits.")
        sys.exit()
    trait = mm.dict_traits[trait_in]["mean"]
    relative = mm.dict_traits[trait_in]["relative"]
    zmatrix = get_zmatrix(t, df, trait)

    if relative == "-none":
        zmatrix = zmatrix - get_zmatrix(t, df_none, trait)
    elif relative == "none-":
        if none:
            zmatrix = 0.5 - zmatrix
        else:
            zmatrix = get_zmatrix(t, df_none, trait) - zmatrix
    elif relative == "-social":
        zmatrix = zmatrix - get_zmatrix(t, df_social, trait)
    elif relative == "given":
        zmatrix = zmatrix * df.iloc[0]["Given"]
    elif relative == "neutral":
        zmatrix = zmatrix - get_zmatrix(t, df, f"Neutral{trait}")
    elif relative == "N":
        n = float(pow(2, get_config("N")))
        zmatrix = zmatrix / n

    return zmatrix
