"""Social dilemmas."""

from .repeat_for_matrix import repeat_for_matrix
from .default_options import default_options


def dilemmas(options):
    """Magnitude of social dilemmas."""

    givens = [["1.0", "1.0"], ["0.5", "0.5"]]

    nrows = len(givens)
    ncols = len(givens[0])

    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, ncols)

    options = default_options(variants, options)

    options["givens"] = givens
    options["givens_control"] = repeat_for_matrix("0.0", nrows, ncols)
    options["titles_columns"] = ["Production of $\\it{B}$", "Fitness"]
    options["traits"] = [["qBSeenmean", "wmean"] for _ in range(nrows)]
    options["traits_control"] = options["traits"]

    return options
