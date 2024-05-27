"""This module sets the data_dict common to all subplots."""

import numpy as np

from common_modules.settings import SETTINGS as project
from modules_icurves.settings import SETTINGS as exclusive


def get_data_dict(data_dict):
    """Data common to all subplots."""

    data_dict["frames"] = np.linspace(0.0, 1.0, num=11)
    data_dict["frames"] = np.append(data_dict["frames"], 0.0)

    data_dict["alphas"] = np.linspace(
        project["alpha_max"],
        project["alpha_min"],
        num=exclusive["nr"],
    )
    data_dict["logess"] = np.linspace(
        project["loges_min"],
        project["loges_max"],
        num=exclusive["nc"],
    )
    data_dict["rhos"] = 1.0 - 1.0 / np.power(2.0, data_dict["logess"])

    return data_dict
