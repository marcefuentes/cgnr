""" Update data in artists. """

import re
import numpy as np
import pandas as pd

from matplotlib import colormaps

from common_modules.get_config import get_config
import modules.modes as mm
import modules.settings as ss


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


def update(t, kwargs):
    """Update the plot with the data at time t."""

    if kwargs["movie"]:
        kwargs["text"].set_text(t)

    for r, _ in enumerate(kwargs["rows"]):
        for c, _ in enumerate(kwargs["columns"]):
            zmatrix = update_zmatrix(t, kwargs, r, c)
            if kwargs["dffrqs"]:
                kwargs["artists"][r, c] = update_histogram(t, kwargs, zmatrix, r, c)
            else:
                kwargs["artists"][r, c].set_array(zmatrix)

    return kwargs["artists"].flatten()


def update_histogram(t, kwargs, zmatrix, r, c):
    """Update the histogram with the data at time t."""

    if kwargs["mode_is_single_trait"]:
        df = kwargs["dffrqs"][r][c]
        trait = mm.dict_traits[kwargs["mode"]]["frq"]
    else:
        df = kwargs["dffrqs"][r]
        trait = mm.dict_traits[kwargs["columns"][0]]["frq"]

    for a, alpha in enumerate(kwargs["alphas"]):
        for e, loges in enumerate(kwargs["logess"]):
            d = df[(df["Time"] == t) & (df["alpha"] == alpha) & (df["logES"] == loges)]
            freq_a = [col for col in d.columns if re.match(rf"^{trait}\d+$", col)]
            y = d.loc[:, freq_a].values[0].flatten()
            kwargs["artists"][r, c, a, e].set_ydata(y)
            bgcolor = colormaps[ss.COLOR_MAP]((zmatrix[a, e] + 1) / 2)
            kwargs["artists"][r, c, a, e].axes.set_facecolor(bgcolor)

    return kwargs["artists"][r, c]


def update_zmatrix(t, kwargs, r, c):
    """Return the updated zmatrix for a given time and trait."""

    if kwargs["mode_is_single_trait"]:
        trait_in = kwargs["mode"]
        df = kwargs["dfs"][r][c]
        df_none = kwargs["df_none"][r][c]
        df_social = kwargs["df_social"][r][c]
    else:
        trait_in = kwargs["columns"][c]
        df_none = kwargs["df_none"]
        df_social = kwargs["df_social"]
        df = kwargs["dfs"][r]

    none = bool(kwargs["rows"][r] == "none" and kwargs["mode"] != "none")

    if "nothing" in trait_in:
        zmatrix = np.zeros((1, 1))
        return zmatrix

    if trait_in not in mm.dict_traits:
        print(f"Trait {trait_in} not in the dictionary.")
        exit()
    trait = mm.dict_traits[trait_in]["mean"]
    relative = mm.dict_traits[trait_in]["relative"]
    zmatrix = get_zmatrix(t, df, trait)

    if relative == "-none":
        zmatrix = zmatrix - get_zmatrix(t, df_none, trait)
        return zmatrix
    if relative == "none-":
        if none:
            zmatrix = 0.5 - zmatrix
        else:
            zmatrix = get_zmatrix(t, df_none, trait) - zmatrix
        return zmatrix
    if relative == "-social":
        zmatrix = zmatrix - get_zmatrix(t, df_social, trait)
        return zmatrix
    if relative == "given":
        zmatrix = zmatrix * df.iloc[0]["Given"]
        return zmatrix
    if relative == "neutral":
        zmatrix = zmatrix - get_zmatrix(t, df, f"Neutral{trait}")
        return zmatrix
    if relative == "N":
        n = float(pow(2, get_config("N")))
        zmatrix = zmatrix / n
        return zmatrix
    return zmatrix
