""" Update data in artists. """

from matplotlib import cm
import numpy as np

from modules_theory.theory import indifference, fitness, qbeq


def update_artists(given, kwargs):
    """Update data in artists."""

    budget_own = kwargs["budget_0"] * (1.0 - given)

    for a, alpha in enumerate(kwargs["alphas"]):
        for r, rho in enumerate(kwargs["rhos"]):

            qb_private = qbeq(given, alpha, rho)

            kwargs["budgets"][a, r].set_ydata(budget_own + qb_private * given)

            w = fitness(qb_private, qb_private, given, alpha, rho)
            kwargs["icurves"][a, r].set_ydata(
                indifference(kwargs["icx"], w, alpha, rho)
            )
            kwargs["icurves"][a, r].set_color(cm.Reds(w))

            kwargs["landscapes"][a, r].set_ydata(
                fitness(qb_private, kwargs["icx"], given, alpha, rho)
            )

    return np.concatenate(
        [
            kwargs["budgets"].flatten(),
            kwargs["icurves"].flatten(),
            kwargs["landscapes"].flatten(),
        ]
    )
