"""8 plots. """

from resultss.layouts.default_options import default_options


def m08(options):
    """4 given=1.0. 4 given=0.5."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    options = default_options(variants, options)

    options["givens"] = [
        ["1.0", "1.0", "1.0"],
        ["1.0", "1.0", "1.0"],
        ["0.5", "0.5", "0.5"],
        ["0.5", "0.5", "0.5"],
    ]

    if options["givens_control"] != "0.0":
        options["givens_control"] = options["givens"]

    return options
