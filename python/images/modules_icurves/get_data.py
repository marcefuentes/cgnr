"""This module sets the data_dict common to all subplots."""

import numpy as np

from settings_icurves.data_constants import data_constants


def get_data(data_dict):
    """Data common to all subplots."""

    data_dict["frames"] = np.linspace(0.0, 1.0, num=11)
    data_dict["frames"] = np.append(data_dict["frames"], 0.0)

    data_dict["alphas"] = np.linspace(
        data_constants["alpha_max"],
        data_constants["alpha_min"],
        num=data_constants["nr"],
    )
    data_dict["logess"] = np.linspace(
        data_constants["loges_min"],
        data_constants["loges_max"],
        num=data_constants["nc"],
    )
    data_dict["rhos"] = 1.0 - 1.0 / np.power(2.0, data_dict["logess"])

    return data_dict
