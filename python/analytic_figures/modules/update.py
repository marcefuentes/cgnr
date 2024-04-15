
""" Update data in artists. """

import re
import numpy as np
import pandas as pd

from matplotlib import colormaps

from common_modules.get_config import get_config
import modules.modes as mm
import modules.settings as ss

def get_zmatrix(t, df, trait):
    """ Returns the zmatrix for a given time, dataframe, and trait. """

    if trait not in df.columns:
        print(f"Trait {trait} not in the dataframe.")
        return None
    m = df.Time == t
    zmatrix = pd.pivot(df.loc[m],
        values=trait,
        index="alpha",
        columns="logES")
    zmatrix = zmatrix.sort_index(axis=0, ascending=False)
    zmatrix = zmatrix.to_numpy()
    return zmatrix

def update_zmatrix(dict_z):
    """ Return the updated zmatrix for a given time and trait. """

    t = dict_z["t"]
    trait_in = dict_z["trait"]
    df = dict_z["df"]
    df_none = dict_z["df_none"]
    df_social = dict_z["df_social"]
    none = dict_z["none"]

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
        zmatrix = zmatrix/n
        return zmatrix
    return zmatrix

def update(t, dict_update):
    """ Update the plot with the data at time t. """

    mode =                  dict_update["mode"]
    mode_is_single_trait =  dict_update["mode_is_single_trait"]
    columns =               dict_update["columns"]
    rows =                  dict_update["rows"]
    dfs =                   dict_update["dfs"]
    df_none =               dict_update["df_none"]
    df_social =             dict_update["df_social"]
    dffrqs =                dict_update["dffrqs"]
    movie =                 dict_update["movie"]
    text =                  dict_update["text"]
    artists =               dict_update["artists"]

    dict_z = {}
    dict_z["t"] = t

    if mode_is_single_trait:
        dict_z["trait"] = mode
    else:
        dict_z["df_none"] = df_none
        dict_z["df_social"] = df_social

    for r, row in enumerate(rows):
        if not mode_is_single_trait:
            dict_z["df"] = dfs[r]
        for c, column in enumerate(columns):
            if mode_is_single_trait:
                dict_z["df"] = dfs[r][c]
                dict_z["df_none"] = df_none[r][c]
                dict_z["df_social"] = df_social[r][c]
            else:
                dict_z["trait"] = column
            if row == "none" and mode != "none":
                dict_z["none"] = True
            else:
                dict_z["none"] = False
            zmatrix = update_zmatrix(dict_z)
            if dffrqs:
                if mode_is_single_trait:
                    trait = mm.dict_traits[mode]["frq"]
                else:
                    trait = mm.dict_traits[column]["frq"]
                for a, alpha in enumerate(dict_update["alphas"]):
                    for e, loges in enumerate(dict_update["logess"]):
                        d = dffrqs[r][
                            (dffrqs[r]["Time"] == t) \
                            & (dffrqs[r]["alpha"] == alpha) \
                            & (dffrqs[r]["logES"] == loges)
                        ]
                        freq_a = [col for col in d.columns if re.match(fr"^{trait}\d+$", col)]
                        y = d.loc[:, freq_a].values[0].flatten()
                        artists[r, c, a, e].set_ydata(y)
                        bgcolor = colormaps[ss.COLOR_MAP]((zmatrix[a, e] + 1) / 2)
                        artists[r, c, a, e].axes.set_facecolor(bgcolor)
            else:
                artists[r, c].set_array(zmatrix)
    if movie:
        text.set_text(t)
    return artists.flatten()
