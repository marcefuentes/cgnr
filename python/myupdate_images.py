
import os
import numpy as np

from myget_Z import get_Z
from mytraits_images import ttr

def update(t, traitset, df_dict, movie, text, artists): 
    traits, _, _ = ttr(traitset)
    for r, key in enumerate(df_dict):
        if (traitset == "cooperation" or traitset == "correlations") and key == "social":
            continue
        for c, trait in enumerate(traits):
            if "nothing" in trait:
                Z = np.zeros((1, 1))
            else:
                Z = get_Z(t, df_dict[key], trait)
            if traitset == "cooperation":
                if "Grain" in trait:
                    if key == "none":
                        Z = 0.5 - Z
                    else:
                        Z = get_Z(t, df_dict["none"], trait) - Z
                else:
                    Z = Z - get_Z(t, df_dict["social"], trait)
            elif traitset == "none":
                if c == 1:
                    given = df_dict[key]["Given"].iloc[0]
                    Z = Z*given
                elif c == 3:
                    Z = Z - get_Z(t, df_dict["social"], trait)
            elif traitset == "correlations":
                if trait == "r_qB_Choose" or trait == "r_qB_Mimic" or trait == "r_qB_Imimic":
                    Z = -Z
            artists[r, c].set_array(Z) 
    if movie:
        text.set_text(t)
    else:
        #text.set_text(os.path.basename(os.getcwd()))
        text.set_text("")

    return artists.flatten()

