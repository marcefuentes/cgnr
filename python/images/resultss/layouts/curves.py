"""Theoretical curves for partner choice and reciprocity."""

from .repeat_for_matrix import repeat_for_matrix
from .default_data import default_data


def curves(data):
    """Fitness curves for partner choice."""

    givens = [["1.0"], ["0.5"], ["0.0"]]

    nrows = len(givens)

    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, 1)

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = givens

    return data
