"""8 plots. """

from resultss.layouts.default_layout import default_layout


def m08(options):
    """4 given=1.0. 4 given=0.5."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    layout = default_layout(variants, options)

    layout["givens"] = [
        ["1.0", "1.0", "1.0"],
        ["1.0", "1.0", "1.0"],
        ["0.5", "0.5", "0.5"],
        ["0.5", "0.5", "0.5"],
    ]

    if options["given_control"] != "0.0":
        layout["givens"] = layout["givens"]

    layout["titles_columns"] = ["No shuffling", "Shuffling"]

    return layout
