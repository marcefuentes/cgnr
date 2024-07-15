"""3 plots."""

from resultss.layouts.default_layout import default_layout


def m04(options):
    """4 plots."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    layout = default_layout(variants, options)

    return layout
