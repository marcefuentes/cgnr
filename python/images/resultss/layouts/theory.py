"""Theory and simulations."""

from .default_options import default_options


def theory(options):
    """First column is theoretical."""

    givens = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]

    nrows = len(givens)

    variants = [[None, "nolang_noshuffle_cost15_4"] for _ in range(nrows)]
    traits = [[None, options["traits"]] for _ in range(nrows)]

    options["givens_control"] = None

    if options["traits"] == "wmean":
        titles = [
            "Fitness\n(theory)",
            "Fitness\n(simulations)",
        ]
    else:
        titles = [
            "Production of $\\it{B}$\n(theory)",
            "Production of $\\it{B}$\n(simulations)",
        ]

    options = default_options(variants, options)

    options["givens"] = givens
    options["mechanisms"] = [[None, "none"] for _ in range(nrows)]
    options["mechanisms_control"] = options["mechanisms"]
    options["titles_columns"] = titles
    options["traits"] = traits

    return options
