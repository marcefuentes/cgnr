""" Update data in artists. """

from matplotlib import cm
import numpy as np

from modules.get_setting import get_setting as get
from modules.theory import fitness, qbeq


def update_artists(given, update_args):
    """Update data in artists."""

    if update_args["movie"]:
        update_args["text"].set_text(f"{given:.2f}")

    budget_own = update_args["budget_0"] * (1.0 - given)

    for a, alpha in enumerate(update_args["alphas"]):
        for r, rho in enumerate(update_args["rhos"]):

            qb_private = qbeq(given, alpha, rho)

            update_args["budgets"][a, r].set_ydata(budget_own + qb_private * given)

            w = fitness(qb_private, qb_private, given, alpha, rho)
            update_args["icurves"][a, r].set_ydata(
                indifference(update_args["icx"], w, alpha, rho)
            )
            update_args["icurves"][a, r].set_color(
                cm.get_cmap(get("COMMON", "color_map"))(0.5 + 0.5 * w)
            )

            update_args["landscapes"][a, r].set_ydata(
                fitness(update_args["icx"], update_args["icx"], 1.0, alpha, rho)
            )

    return np.concatenate(
        [
            update_args["budgets"].flatten(),
            update_args["icurves"].flatten(),
            update_args["landscapes"].flatten(),
        ]
    )


def indifference(qs, w, alpha, rho):
    """Compute indifference curves."""

    q_b = np.full(qs.shape, 1000.0)
    for i, q in enumerate(qs):
        if rho == 0.0:
            q_b[i] = pow(w / pow(q, 1.0 - alpha), 1.0 / alpha)
        else:
            numerator = pow(w, rho) - (1.0 - alpha) * pow(q, rho)
            if numerator <= 0.0:
                if rho < 0.0:
                    q_b[i] = 1000.0
                else:
                    q_b[i] = -0.1
            else:
                q_b[i] = pow(numerator / alpha, 1.0 / rho)
    return q_b
