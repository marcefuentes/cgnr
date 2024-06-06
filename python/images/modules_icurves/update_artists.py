""" Update data in artists. """

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

from modules.theory import fitness, indifference, qbeq


def update_artists(given, update_args, options, dynamic_data):
    """Update data in artists."""

    if options["movie"]:
        dynamic_data["text"].set_text(f"{given:.2f}")

    budget_own = (1.0 - dynamic_data["x_values"]) * (1.0 - given)

    for i, alpha in enumerate(dynamic_data["alphas"]):
        for j, rho in enumerate(dynamic_data["rhos"]):

            qb_private = qbeq(given, alpha, rho)
            update_args["budgets"][i, j].set_ydata(budget_own + qb_private * given)

            w = fitness(qb_private, qb_private, given, alpha, rho)
            update_args["icurves"][i, j].set_ydata(
                indifference(dynamic_data["x_values"], w, alpha, rho)
            )
            update_args["icurves"][i, j].set_color(
                cm.get_cmap(update_args["cmap"])(0.5 + 0.5 * w)
            )

            y = fitness(
                dynamic_data["x_values"], dynamic_data["x_values"], given, alpha, rho
            )
            points = np.array([dynamic_data["x_values"], y]).T.reshape((-1, 1, 2))
            update_args["landscapes"][i, j].set_segments(
                np.concatenate([points[:-1], points[1:]], axis=1)
            )
            update_args["landscapes"][i, j].set_array(y)
            update_args["landscapes"][i, j].set_cmap(cm.get_cmap(update_args["cmap"]))
            update_args["landscapes"][i, j].set_norm(plt.Normalize(-1, 1))

    return np.concatenate(
        [
            update_args["budgets"].flatten(),
            update_args["icurves"].flatten(),
            update_args["landscapes"].flatten(),
        ]
    )
