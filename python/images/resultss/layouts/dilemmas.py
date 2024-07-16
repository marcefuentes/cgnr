"""Social dilemmas."""

from .repeat_for_matrix import repeat_for_matrix
from .default_data import default_data


def dilemmas(data):
    """Magnitude of social dilemmas."""

    givens = [["1.0", "1.0"], ["0.5", "0.5"]]

    nrows = len(givens)
    ncols = len(givens[0])

    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, ncols)

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = repeat_for_matrix("0.0", nrows, ncols)
    data["titles_columns"] = ["Production of $\\it{B}$", "Fitness"]
    data["traits"] = [["qBSeenmean", "wmean"] for _ in range(nrows)]
    data["traits_control"] = data["traits"]

    return data
