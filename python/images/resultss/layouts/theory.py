"""Theory and simulations."""

from resultsm.add_default_data import add_default_data


def theory(data):
    """First column is theoretical."""

    givens = [[1.0, "1.0"], [0.5, "0.5"], [0.0, "0.0"]]

    variants = [["nothing", "nolang_noshuffle_cost15_4"] for _ in givens]
    trait = data["traits"]

    data["givens_control"] = "nothing"

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

    add_default_data(data, variants)

    data["givens"] = givens
    data["titles_columns"] = titles
