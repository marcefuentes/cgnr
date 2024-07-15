"""Theoretical curves for partner choice and reciprocity."""

from resultsm.repeat_for_matrix import repeat_for_matrix
from resultss.layouts.default_options import default_options


def curves(options):
    """Fitness curves for partner choice."""

    givens = [["1.0"], ["0.5"], ["0.0"]]

    nrows = len(givens)

    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, 1)

    options = default_options(variants, options)

    options["givens"] = givens
    options["givens_control"] = givens

    return options
