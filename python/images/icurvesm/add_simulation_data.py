"""Add givens, alphas and rhos."""

import numpy as np


def add_simulation_data(data):
    """Add givens, alphas and rhos."""

    data["alphas"] = np.linspace(**data["alphas_params"])
    data["logess"] = np.linspace(**data["logess_params"])
    if data["movie"]:
        data["frames"] = np.concatenate([np.linspace(**data["frames_params"]), [0.0]])
    else:
        data["frames"] = [0.0]
    data["rhos"] = 1.0 - 1.0 / np.power(2.0, data["logess"])
