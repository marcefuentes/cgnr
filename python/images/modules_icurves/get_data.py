"""This module sets the data common to all subplots."""

import numpy as np


def get_data(data_constants):
    """Data common to all subplots."""

    data = {}

    data["frames"] = np.linspace(0.0, 1.0, num=11)
    data["frames"] = np.append(data["frames"], 0.0)

    data["alphas"] = np.linspace(
        data_constants["alpha_max"],
        data_constants["alpha_min"],
        num=data_constants["nr"],
    )
    data["logess"] = np.linspace(
        data_constants["loges_min"],
        data_constants["loges_max"],
        num=data_constants["nc"],
    )
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])

    return data
