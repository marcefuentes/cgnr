"""8 plots. """

from resultss.layouts.default_layout import default_layout


def m08(options):
    """4 relative to none. 4 relative to social."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    layout = default_layout(variants, options)

    layout["givens_control"] = [
        [options["given"], options["given"]],
        [options["given"], options["given"]],
        ["0.0", "0.0"],
        ["0.0", "0.0"],
    ]

    layout["titles_columns"] = ["No shuffling", "Shuffling"]

    return layout
