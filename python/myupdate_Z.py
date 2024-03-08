
import numpy as np
import pandas as pd

def get_Z(t, df, trait):
    m = df.Time == t
    Z = pd.pivot(df.loc[m],
                 values=trait,
                 index="alpha",
                 columns="logES")
    Z = Z.sort_index(axis=0, ascending=False)
    Z = Z.to_numpy()
    return Z

def update_Z(t, df_dict, key, trait, traitset): 
    if "nothing" in trait:
        Z = np.zeros((1, 1))
    elif "r_" in trait:
        Z = get_Z(t, df_dict[key], trait)
    elif "byproduct" in trait:
        Z = get_Z(t, df_dict[key], "qBmean")
    elif "deficit" in trait:
        Z = get_Z(t, df_dict[key], "wmean")
    else:
        Z = get_Z(t, df_dict[key], f"{trait}mean")
    if "cooperation" in traitset:
        if "Grain" in trait:
            if key == "none":
                Z = 0.5 - Z
            else:
                Z = get_Z(t, df_dict["none"], f"{trait}mean") - Z
        else:
            Z = Z - get_Z(t, df_dict["social"], f"{trait}mean")
    elif traitset == "none":
        if "byproduct" in trait:
            given = df_dict[key]["Given"].iloc[0]
            Z = Z * given
        elif "deficit" in trait:
            Z = Z - get_Z(t, df_dict["social"], "wmean")
    elif traitset == "demography":
        if "Dispersal" in trait:
            Z = Z - get_Z(t, df_dict[key], "NeutralDispersalRatemean")
        elif "N" in trait:
            Z = Z/4096.0
    elif traitset == "correlations":
        if trait == "r_qB_Choose" or trait == "r_qB_Mimic" or trait == "r_qB_Imimic":
            Z = -Z
    return Z

