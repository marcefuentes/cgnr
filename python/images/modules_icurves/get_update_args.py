"""This module sets the update_args common to all subplots."""

import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get


def get_update_args(update_args):
    """Data common to all subplots."""

    update_args["frames"] = np.linspace(0.0, 1.0, num=11)
    update_args["frames"] = np.append(update_args["frames"], 0.0)

    update_args["alphas"] = np.linspace(
        get_config("alpha_max"),
        get_config("alpha_min"),
        num=get(update_args["file_name"], "nr"),
    )
    update_args["logess"] = np.linspace(
        get_config("loges_min"),
        get_config("loges_max"),
        num=get(update_args["file_name"], "nc"),
    )
    update_args["rhos"] = 1.0 - 1.0 / np.power(2.0, update_args["logess"])
    update_args["x_values"] = np.linspace(
        0.001, 0.999, num=get(update_args["file_name"], "n_x_values")
    )

    return update_args
