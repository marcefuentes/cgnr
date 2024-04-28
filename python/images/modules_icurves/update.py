""" Update data in artists. """

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

from modules.get_setting import get_setting as get
from modules.theory import fitness, indifference, qbeq


def update_artists(given, update_args):
    """Update data in artists."""

    if update_args["movie"]:
        update_args["text"].set_text(f"{given:.2f}")

    budget_own = (1.0 - update_args["x_values"]) * (1.0 - given)

    for i, alpha in enumerate(update_args["alphas"]):
        for j, rho in enumerate(update_args["rhos"]):

            if not update_args["movie"]:
                given = 0.0

            qb_private = qbeq(given, alpha, rho)
            update_args["budgets"][i, j].set_ydata(budget_own + qb_private * given)

            w = fitness(qb_private, qb_private, given, alpha, rho)
            update_args["icurves"][i, j].set_ydata(
                indifference(update_args["x_values"], w, alpha, rho)
            )
            update_args["icurves"][i, j].set_color(
                cm.get_cmap(get("COMMON", "color_map"))(0.5 + 0.5 * w)
            )

            if not update_args["movie"]:
                given = 1.0

            qb_private = qbeq(given, alpha, rho)
            qb_social = qbeq(0.0, alpha, rho)

            y = fitness(update_args["x_values"], qb_social, given, alpha, rho)
            points = np.array([update_args["x_values"], y]).T.reshape((-1, 1, 2))
            update_args["social_landscapes"][i, j].set_segments(
                np.concatenate([points[:-1], points[1:]], axis=1)
            )
            update_args["social_landscapes"][i, j].set_array(y)
            update_args["social_landscapes"][i, j].set_cmap(
                cm.get_cmap(get("COMMON", "color_map"))
            )
            update_args["social_landscapes"][i, j].set_norm(plt.Normalize(-1, 1))

            y = fitness(update_args["x_values"], qb_private, given, alpha, rho)
            points = np.array([update_args["x_values"], y]).T.reshape((-1, 1, 2))
            update_args["private_landscapes"][i, j].set_segments(
                np.concatenate([points[:-1], points[1:]], axis=1)
            )
            update_args["private_landscapes"][i, j].set_array(y)
            update_args["private_landscapes"][i, j].set_cmap(
                cm.get_cmap(get("COMMON", "color_map"))
            )
            update_args["private_landscapes"][i, j].set_norm(plt.Normalize(-1, 1))

    return np.concatenate(
        [
            update_args["budgets"].flatten(),
            update_args["icurves"].flatten(),
            update_args["social_landscapes"].flatten(),
            update_args["private_landscapes"].flatten(),
        ]
    )
