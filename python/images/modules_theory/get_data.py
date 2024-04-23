"""This module sets the data common to all subplots."""

import numpy as np

from common_modules.get_config import get_config
from modules_theory.theory import indifference
import modules_theory.settings as ss


def get_data():
    """Data common to all subplots."""

    givens = np.linspace(0.0, 1.0, num=10)
    givens = np.append(givens, 0.0)
    alphas = np.linspace(get_config("alpha_max"), get_config("alpha_min"), num=ss.NC)
    logess = np.linspace(get_config("loges_min"), get_config("loges_max"), num=ss.NC)
    rhos = 1.0 - 1.0 / np.power(2.0, logess)
    icx = np.linspace(0.001, 0.999, num=ss.N_X_VALUES)
    budget_0 = 1.0 - icx

    w_isoclines = np.linspace(1.0 / (ss.N_IC + 1), ss.N_IC / (ss.N_IC + 1), num=ss.N_IC)

    isoclines = np.zeros((ss.NC, ss.NC, ss.N_IC, ss.N_X_VALUES))
    for i, alpha in enumerate(alphas):
        for j, rho in enumerate(rhos):
            for k, w in enumerate(w_isoclines):
                isoclines[i, j, k] = indifference(icx, w, alpha, rho)

    data = {
        "alphas": alphas,
        "logess": logess,
        "rhos": rhos,
        "icx": icx,
        "budget_0": budget_0,
        "isoclines": isoclines,
    }

    return givens, data
