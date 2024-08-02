"""Theoretical curves for partner choice and reciprocity."""

from .default_data import default_data


def curves(data):
    """Fitness curves for partner choice."""

    givens = [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]]

    nrows = len(givens)

    variants = [["nothing", "nolang_noshuffle_cost15_4"] for _ in range(nrows)]

    default_data(data, variants)

    data["givens"] = givens
    data["givens_control"] = givens
