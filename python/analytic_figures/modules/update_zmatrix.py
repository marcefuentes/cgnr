
""" Update the zmatrix for a given time and trait. """

import numpy as np
import pandas as pd

from common_modules.get_config import get_config
import modules.modes as mm

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
        zmatrix = zmatrix * mm.GIVEN_FOLDER
        return zmatrix
    if relative == "neutral":
        zmatrix = zmatrix - get_zmatrix(t, df, f"Neutral{trait}")
        return zmatrix
    if relative == "N":
        N = float(pow(2, get_config("N")))
        zmatrix = zmatrix/N
        return zmatrix
    return zmatrix
