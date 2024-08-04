""" Calculates theoretical values for AxesImage. """

from numpy import zeros
from modules.theory import calculate_fitness, qbeq


def artists_theory(data):
    """Calculates theoretical values for AxesImage."""

    trait = data["traits"][0][1]

    y = zeros((data["layout_k"], data["layout_m"]))

    for i, givens_row in enumerate(data["givens"]):
        given = float(givens_row[1])
        for k, alpha in enumerate(data["alphas"]):
            for m, rho in enumerate(data["rhos"]):
                y[k, m] = process(trait, given, alpha, rho)
        data["artists"][i, 0, 0, 0].set_array(y)


def process(trait, given, alpha, rho):
    """Processes the plot."""

    qb = qbeq(given, alpha, rho)
    if trait == "qBSeenmean":
        return qb
    return calculate_fitness(qb, qb, given, alpha, rho)
