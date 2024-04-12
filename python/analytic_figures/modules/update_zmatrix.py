
""" Update the zmatrix for a given mechanism, trait, and mode. """

import numpy as np
import pandas as pd

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

    t = dict_z["t"]
    mode = dict_z["mode"]
    mechanism = dict_z["row"]
    trait = dict_z["trait"]
    df = dict_z["df"]
    df_none = dict_z["df_none"]
    df_social = dict_z["df_social"]

    if "nothing" in trait:
        zmatrix = np.zeros((1, 1))
        return zmatrix

    if "r_" in trait:
        zmatrix = get_zmatrix(t, df, trait)
    elif "byproduct" in trait:
        zmatrix = get_zmatrix(t, df, "qBmean")
    elif "deficit" in trait:
        zmatrix = get_zmatrix(t, df, "wmean")
    else:
        zmatrix = get_zmatrix(t, df, f"{trait}mean")

    if "cooperation" in mode:
        if "Grain" in trait:
            if mechanism == "none":
                zmatrix = 0.5 - zmatrix
            else:
                zmatrix = get_zmatrix(t, df_none, f"{trait}mean") - zmatrix
        else:
            zmatrix = zmatrix - get_zmatrix(t, df_social, f"{trait}mean")
    elif mode == "none":
        if "byproduct" in trait:
            given = df_dict[mechanism]["Given"].iloc[0]
            zmatrix = zmatrix * given
        elif "deficit" in trait:
            zmatrix = zmatrix - get_zmatrix(t, df_social, "wmean")
    elif mode == "demography":
        if "Dispersal" in trait:
            zmatrix = zmatrix - get_zmatrix(t, df, "NeutralDispersalRatemean")
        elif "N" in trait:
            zmatrix = zmatrix/4096.0

    return zmatrix
