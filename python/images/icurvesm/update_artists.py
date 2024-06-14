""" Update data in artists. """

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

from modules.theory import fitness, indifference, qbeq


def update_artists(given_movie, update_args, options, data):
    """Update data in artists."""

    if options["movie"]:
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
                update_args["landscapes"][i, 0, j, k].set(
                    array=y,
                    cmap=cm.get_cmap(update_args["cmap"]),
                    norm=plt.Normalize(-1, 1),
                    segments=np.concatenate([points[:-1], points[1:]], axis=1),
                )

                y = (budget_own + qb_partner * given) * options["budget_line"]
                update_args["budgets"][i, 0, j, k].set(ydata=y)

                y = fitness(qb_partner, qb_partner, given, alpha, rho)
                update_args["icurves"][i, 0, j, k].set(
                    ydata=indifference(data["x_values"], y, alpha, rho),
                    color=cm.get_cmap(update_args["cmap"])(0.5 + 0.5 * y),
                )

    return np.concatenate(
        [
            update_args["budgets"].flatten(),
            update_args["icurves"].flatten(),
            update_args["landscapes"].flatten(),
        ]
    )
