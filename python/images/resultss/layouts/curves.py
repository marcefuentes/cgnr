"""Theoretical curves for partner choice and reciprocity."""

from resultsm.add_default_data import add_default_data


def curves(data):
    """Fitness curves for partner choice."""

    givens = [[1.0, "1.0"], [0.5, "0.5"], [0.0, "0.0"]]

    variants = [["nothing", "nolang_noshuffle_cost15_4"] for _ in givens]

    add_default_data(data, variants)

    data["givens"] = givens
    data["givens_control"] = givens
