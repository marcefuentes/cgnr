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

                qb_private = qbeq(given, alpha, rho)
                update_args["budgets"][i, j, k].set_ydata(
                    budget_own + qb_private * given
                )

                w = fitness(qb_private, qb_private, given, alpha, rho)
                update_args["icurves"][i, j, k].set(
                    ydata=indifference(data["x_values"], w, alpha, rho),
                    color=cm.get_cmap(update_args["cmap"])(0.5 + 0.5 * w),
                )

                y = fitness(
                    np.full((data["n_x_values"]), qb_private),
                    data["x_values"],
                    given,
                    alpha,
                    rho,
                )
                points = np.array([data["x_values"], y]).T.reshape((-1, 1, 2))
                update_args["landscapes"][i, j, k].set_segments(
                    np.concatenate([points[:-1], points[1:]], axis=1)
                )
                update_args["landscapes"][i, j, k].set(
                    array=y,
                    cmap=cm.get_cmap(update_args["cmap"]),
                    norm=plt.Normalize(-1, 1),
                )

    return np.concatenate(
        [
            update_args["budgets"].flatten(),
            update_args["icurves"].flatten(),
            update_args["icurves_grey"].flatten(),
            update_args["landscapes"].flatten(),
        ]
    )
