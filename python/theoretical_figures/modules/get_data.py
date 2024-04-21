"""This module sets the data common to all subplots."""

import numpy as np

from common_modules.get_config import get_config
import modules.settings as ss


def get_data():
    """Data common to all subplots."""

    logess = np.linspace(get_config("loges_min"), get_config("loges_max"), num=ss.NC)
    rhos = 1.0 - 1.0 / np.power(2.0, logess)

    data = {
        "alphas": np.linspace(get_config("alpha_max"), get_config("alpha_min"), num=ss.NC),
        "logess": logess,
        "rhos": rhos,
        "x_data": np.linspace(0.001, 0.999, num=ss.VALUES_PER_CURVE),
        "w_isoclines": np.linspace(1.0/(ss.N_IC+1), 1.0 - 1.0/ss.N_IC, num=ss.N_IC),
    }
    return data
