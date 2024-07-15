"""Two plots."""

from resultsm.repeat_for_matrix import repeat_for_matrix
from resultss.layouts.default_layout import default_layout


def m02(options):
    """Two plots."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_shuffle_cost15_128"],
        [f"{lang}_shuffle_cost15_4"],
    ]

    layout = default_layout(variants, options)

    layout["titles_columns"] = ["Shuffling"]

    return layout
