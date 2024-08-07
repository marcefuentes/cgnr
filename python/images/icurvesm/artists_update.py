""" Update data in artists. """

from matplotlib.pyplot import Normalize
import numpy as np

from modules.theory import get_fitness, get_fitness_curve, get_icurves, get_qbeq


def artists_update(given_movie, data):
    """Update data in artists."""

    if data["movie"]:
        data["text"].set_text(f"{given_movie:.2f}")
        givens = [given_movie]
    else:
        givens = data["givens"]

    for i, given in enumerate(givens):
        budget_own = (1.0 - data["x"]) * (1.0 - given)
        for j, alpha in enumerate(data["alphas"]):
            for k, rho in enumerate(data["rhos"]):

                qb_partner = get_qbeq(given, alpha, rho)

                y = get_fitness_curve(
                    np.full((len(data["x"])), qb_partner),
                    data["x"],
                    given,
                    alpha,
                    rho,
                )
                points = np.array([data["x"], y]).T.reshape((-1, 1, 2))
                data["landscapes"][i, 0, j, k].set(
                    array=y,
                    cmap=data["color_map"],
                    norm=Normalize(-1, 1),
                    segments=np.concatenate([points[:-1], points[1:]], axis=1),
                )

                y = (budget_own + qb_partner * given) * data["budget_line"]
                data["budgets"][i, 0, j, k].set(ydata=y)

                y = get_fitness(qb_partner, qb_partner, given, alpha, rho)
                data["icurves"][i, 0, j, k].set(
                    ydata=get_icurves(data["x"], y, alpha, rho),
                    color=data["color_map"](0.5 + 0.5 * y),
                )

    return np.concatenate(
        [
            data["budgets"].flatten(),
            data["icurves"].flatten(),
            data["landscapes"].flatten(),
        ]
    )
