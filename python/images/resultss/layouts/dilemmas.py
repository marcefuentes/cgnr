"""Social dilemmas."""

from modules.fill_matrix import fill_matrix
from resultsm.default_data import default_data


def dilemmas(data):
    """Magnitude of social dilemmas."""

    givens = [["1.0", "1.0"], ["0.5", "0.5"]]

    variants = fill_matrix("nolang_noshuffle_cost15_4", givens)

    default_data(data, variants)

    data["givens"] = givens
    data["givens_control"] = fill_matrix("0.0", givens)
    data["titles_columns"] = ["Production of $\\it{B}$", "Fitness"]
    data["traits"] = [["qBSeenmean", "wmean"] for _ in givens]
    data["traits_control"] = data["traits"]
