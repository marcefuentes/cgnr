"""This module sets the data common to all subplots."""

import numpy as np

from common_modules.get_config import get_config
from modules_theory.theory import indifference
import modules_theory.settings as ss


def get_data(data):
    """Data common to all subplots."""

    givens = np.linspace(0.0, 1.0, num=10)
    givens = np.append(givens, 0.0)

    data["alphas"] = np.linspace(
        get_config("alpha_max"), get_config("alpha_min"), num=ss.NC
    )
    data["logess"] = np.linspace(
        get_config("loges_min"), get_config("loges_max"), num=ss.NC
    )
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])
    data["icx"] = np.linspace(0.001, 0.999, num=ss.N_X_VALUES)
    data["budget_0"] = 1.0 - data["icx"]

    w_isoclines = np.linspace(1.0 / (ss.N_IC + 1), ss.N_IC / (ss.N_IC + 1), num=ss.N_IC)

    data["isoclines"] = np.zeros((ss.NC, ss.NC, ss.N_IC, ss.N_X_VALUES))
    for i, alpha in enumerate(data["alphas"]):
        for j, rho in enumerate(data["rhos"]):
            for k, w in enumerate(w_isoclines):
                data["isoclines"][i, j, k] = indifference(data["icx"], w, alpha, rho)

    return givens, data
