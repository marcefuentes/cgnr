"""This module sets the update_args common to all subplots."""

import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get
from modules_icurves.update import indifference


def get_update_args(update_args):
    """Data common to all subplots."""

    update_args["frames"] = np.linspace(0.0, 1.0, num=11)
    update_args["frames"] = np.append(update_args["frames"], 0.0)

    update_args["alphas"] = np.linspace(
        get_config("alpha_max"),
        get_config("alpha_min"),
        num=get(update_args["file_name"], "nc"),
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

    w_isoclines = np.linspace(
        1.0 / (get(update_args["file_name"], "n_ic") + 1),
        get(update_args["file_name"], "n_ic")
        / (get(update_args["file_name"], "n_ic") + 1),
        num=get(update_args["file_name"], "n_ic"),
    )

    update_args["isoclines"] = np.zeros(
        (
            get(update_args["file_name"], "nc"),
            get(update_args["file_name"], "nc"),
            get(update_args["file_name"], "n_ic"),
            get(update_args["file_name"], "n_x_values"),
        )
    )
    for i, alpha in enumerate(update_args["alphas"]):
        for j, rho in enumerate(update_args["rhos"]):
            for k, w in enumerate(w_isoclines):
                update_args["isoclines"][i, j, k] = indifference(
                    update_args["x_values"], w, alpha, rho
                )

    return update_args
