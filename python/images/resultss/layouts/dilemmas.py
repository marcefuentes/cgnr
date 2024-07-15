"""Social dilemmas."""

from resultsm.repeat_for_matrix import repeat_for_matrix
from resultss.layouts.default_layout import default_layout


def dilemmas(options):
    """Magnitude of social dilemmas."""

    givens = [["1.0", "1.0"], ["0.5", "0.5"]]

    nrows = len(givens)
    ncols = len(givens[0])

    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, ncols)

    traits = [["qBSeenmean", "wmean"] for _ in range(nrows)]

    layout = default_layout(variants, options)

    layout["givens"] = givens
    layout["givens_control"] = repeat_for_matrix("0.0", nrows, ncols)
    layout["titles_columns"] = ["Production of $\\it{B}$", "Fitness"]
    layout["traits"] = traits
    layout["traits_control"] = traits

    return layout
