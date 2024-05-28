""" Update data in artists. """

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

from modules.theory import fitness, indifference, qbeq
from settings_icurves.image import image


def update_artists(given, data_dict):
    """Update data in artists."""

    if data_dict["movie"]:
        data_dict["text"].set_text(f"{given:.2f}")

    budget_own = (1.0 - data_dict["x_values"]) * (1.0 - given)

    for i, alpha in enumerate(data_dict["alphas"]):
        for j, rho in enumerate(data_dict["rhos"]):

            qb_private = qbeq(given, alpha, rho)
            data_dict["budgets"][i, j].set_ydata(budget_own + qb_private * given)

            w = fitness(qb_private, qb_private, given, alpha, rho)
            data_dict["icurves"][i, j].set_ydata(
                indifference(data_dict["x_values"], w, alpha, rho)
            )
            data_dict["icurves"][i, j].set_color(
                cm.get_cmap(image["color_map"])(0.5 + 0.5 * w)
            )

            y = fitness(data_dict["x_values"], data_dict["x_values"], given, alpha, rho)
            points = np.array([data_dict["x_values"], y]).T.reshape((-1, 1, 2))
            data_dict["landscapes"][i, j].set_segments(
                np.concatenate([points[:-1], points[1:]], axis=1)
            )
            data_dict["landscapes"][i, j].set_array(y)
            data_dict["landscapes"][i, j].set_cmap(cm.get_cmap(image["color_map"]))
            data_dict["landscapes"][i, j].set_norm(plt.Normalize(-1, 1))

    return np.concatenate(
        [
            data_dict["budgets"].flatten(),
            data_dict["icurves"].flatten(),
            data_dict["landscapes"].flatten(),
        ]
    )
