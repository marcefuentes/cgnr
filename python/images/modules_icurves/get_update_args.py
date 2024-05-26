"""This module sets the update_args common to all subplots."""

import numpy as np

from common_modules.settings import SETTINGS as project
from modules_icurves.settings import SETTINGS as exclusive


def get_update_args(update_args):
    """Data common to all subplots."""

    update_args["frames"] = np.linspace(0.0, 1.0, num=11)
    update_args["frames"] = np.append(update_args["frames"], 0.0)

    update_args["alphas"] = np.linspace(
        project["alpha_max"],
        project["alpha_min"],
        num=exclusive["nr"],
    )
    update_args["logess"] = np.linspace(
        project["loges_min"],
        project["loges_max"],
        num=exclusive["nc"],
    )
    update_args["rhos"] = 1.0 - 1.0 / np.power(2.0, update_args["logess"])

    return update_args
