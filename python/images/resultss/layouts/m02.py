"""Two plots."""

from .default_options import default_options


def m02(options):
    """Two plots."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_shuffle_cost15_128"],
        [f"{lang}_shuffle_cost15_4"],
    ]

    options = default_options(variants, options)

    return options
