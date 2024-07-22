"""Theory and simulations."""

from .default_data import default_data


def theory(data):
    """First column is theoretical."""

    givens = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]

    nrows = len(givens)

    variants = [[None, "nolang_noshuffle_cost15_4"] for _ in range(nrows)]
    traits = [[None, data["traits"]] for _ in range(nrows)]

    data["givens_control"] = None

    if data["traits"] == "wmean":
        titles = [
            "Fitness\n(theory)",
            "Fitness\n(simulations)",
        ]
    else:
        titles = [
            "Production of $\\it{B}$\n(theory)",
            "Production of $\\it{B}$\n(simulations)",
        ]

    default_data(data, variants)

    data["givens"] = givens
    data["mechanisms"] = [[None, "none"] for _ in range(nrows)]
    data["mechanisms_control"] = data["mechanisms"]
    data["titles_columns"] = titles
    data["traits"] = traits
