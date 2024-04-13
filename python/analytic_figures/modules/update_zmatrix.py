
""" Update the zmatrix for a given mechanism, trait, and mode. """

import numpy as np
import pandas as pd

import modules.modes as mm
from common_modules.get_config import get_config

def get_zmatrix(t, df, trait):
    """ Returns the zmatrix for a given time, dataframe, and trait. """

    m = df.Time == t
    zmatrix = pd.pivot(df.loc[m],
        values=trait,
        index="alpha",
        columns="logES")
    zmatrix = zmatrix.sort_index(axis=0, ascending=False)
    zmatrix = zmatrix.to_numpy()
    return zmatrix

def update_zmatrix(dict_z):
    """ Return the updated zmatrix for a given time,
    dataframe dictionary, mechanism, trait, and mode. """

    t =             dict_z["t"]
    mode =          dict_z["mode"]
    mechanism =     dict_z["mechanism"]
    trait_in =      dict_z["trait"]
    df =            dict_z["df"]
    df_none =       dict_z["df_none"]
    df_social =     dict_z["df_social"]

    if "nothing" in trait_in:
        zmatrix = np.zeros((1, 1))
        return zmatrix

    trait = mm.look_in(mm.dict_traits, trait_in, "mean")
    relative = mm.look_in(mm.dict_traits, trait_in, "relative")
    zmatrix = get_zmatrix(t, df, trait)

    if relative == "-none":
        zmatrix = zmatrix - get_zmatrix(t, df_none, trait)
        return zmatrix
    if relative == "none-":
        zmatrix = get_zmatrix(t, df_none, trait) - zmatrix
        return zmatrix
    if relative == "-social":
        zmatrix = zmatrix - get_zmatrix(t, df_social, trait)
        return zmatrix
    if relative == "given":
        zmatrix = zmatrix * mm.given
        return zmatrix
    if relative == "neutral":
        zmatrix = zmatrix - get_zmatrix(t, df, f"{Neutral}{trait}")
        return zmatrix
    if relative == "N":
        zmatrix = zmatrix/get_config("N")
        return zmatrix
    return zmatrix
