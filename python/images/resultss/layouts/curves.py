"""Theoretical curves for partner choice and reciprocity."""

from resultsm.repeat_for_matrix import repeat_for_matrix
from resultss.layouts.default_layout import default_layout

def curves(options):
    """Fitness curves for partner choice."""

    givens = [["1.0"], ["0.5"], ["0.0"]]

    nrows = len(givens)

    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, 1)

    layout = default_layout(variants, options)

    layout["givens"] = givens
    layout["givens_control"] = givens

    return layout
