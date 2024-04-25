"""This module sets the data common to all subplots."""

import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get
from modules_icurves.update import indifference


def get_data(file_name, data):
    """Data common to all subplots."""

    givens = np.linspace(0.0, 1.0, num=11)
    givens = np.append(givens, 0.0)

    data["alphas"] = np.linspace(
        get_config("alpha_max"), get_config("alpha_min"), num=get(file_name, "nc")
    )
    data["logess"] = np.linspace(
        get_config("loges_min"), get_config("loges_max"), num=get(file_name, "nc")
    )
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])
    data["icx"] = np.linspace(0.001, 0.999, num=get(file_name, "n_x_values"))
    data["budget_0"] = 1.0 - data["icx"]

    w_isoclines = np.linspace(
        1.0 / (get(file_name, "n_ic") + 1),
        get(file_name, "n_ic") / (get(file_name, "n_ic") + 1),
        num=get(file_name, "n_ic"),
    )

    data["isoclines"] = np.zeros(
        (
            get(file_name, "nc"),
            get(file_name, "nc"),
            get(file_name, "n_ic"),
            get(file_name, "n_x_values"),
        )
    )
    for i, alpha in enumerate(data["alphas"]):
        for j, rho in enumerate(data["rhos"]):
            for k, w in enumerate(w_isoclines):
                data["isoclines"][i, j, k] = indifference(data["icx"], w, alpha, rho)

    return givens, data
