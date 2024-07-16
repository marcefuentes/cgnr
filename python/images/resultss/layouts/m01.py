"""Single plot."""

from .default_options import default_options


def m01(options):
    """Single plot."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [[f"{lang}_noshuffle_cost15_4"]]

    options = default_options(variants, options)

    return options
