"""This module sets the dynamic_data common to all subplots."""

import numpy as np

from settings_icurves.data_constants import data_constants


def get_data(dynamic_data):
    """Data common to all subplots."""

    dynamic_data["frames"] = np.linspace(0.0, 1.0, num=11)
    dynamic_data["frames"] = np.append(dynamic_data["frames"], 0.0)

    dynamic_data["alphas"] = np.linspace(
        data_constants["alpha_max"],
        data_constants["alpha_min"],
        num=data_constants["nr"],
    )
    dynamic_data["logess"] = np.linspace(
        data_constants["loges_min"],
        data_constants["loges_max"],
        num=data_constants["nc"],
    )
    dynamic_data["rhos"] = 1.0 - 1.0 / np.power(2.0, dynamic_data["logess"])

    return dynamic_data
