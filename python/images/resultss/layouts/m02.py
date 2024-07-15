"""Two plots."""

from resultss.layouts.default_layout import default_layout


def m02(options):
    """Two plots."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_shuffle_cost15_128"],
        [f"{lang}_shuffle_cost15_4"],
    ]

    layout = default_layout(variants, options)

    return layout
