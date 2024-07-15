"""3 plots."""

from resultss.layouts.default_options import default_options


def m04(options):
    """4 plots."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    options = default_options(variants, options)

    return options
