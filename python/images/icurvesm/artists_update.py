""" Update data in artists. """

import matplotlib.pyplot as plt
import numpy as np

from modules.theory import fitness, indifference, qbeq


def artists_update(given_movie, data):
    """Update data in artists."""

    if data["movie"]:
        data["text"].set_text(f"{given_movie:.2f}")
        givens = [given_movie]
    else:
        givens = data["givens"]

    for i, given in enumerate(givens):
        budget_own = (1.0 - data["x_values"]) * (1.0 - given)
        for j, alpha in enumerate(data["alphas"]):
            for k, rho in enumerate(data["rhos"]):

                qb_partner = qbeq(given, alpha, rho)

                y = fitness(
                    np.full((len(data["x_values"])), qb_partner),
                    data["x_values"],
                    given,
                    alpha,
                    rho,
                )
                points = np.array([data["x_values"], y]).T.reshape((-1, 1, 2))
                data["landscapes"][i, 0, j, k].set(
                    array=y,
                    cmap=plt.get_cmap(data["color_map"]),
                    norm=plt.Normalize(-1, 1),
                    segments=np.concatenate([points[:-1], points[1:]], axis=1),
                )

                y = (budget_own + qb_partner * given) * data["budget_line"]
                data["budgets"][i, 0, j, k].set(ydata=y)

                y = fitness(qb_partner, qb_partner, given, alpha, rho)
                data["icurves"][i, 0, j, k].set(
                    ydata=indifference(data["x_values"], y, alpha, rho),
                    color=plt.get_cmap(data["color_map"])(0.5 + 0.5 * y),
                )

    return np.concatenate(
        [
            data["budgets"].flatten(),
            data["icurves"].flatten(),
            data["landscapes"].flatten(),
        ]
    )
