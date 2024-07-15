"""5 plots."""

from resultss.layouts.default_options import default_options
from resultss.layouts.m10 import m10


def m05(options):
    """1 + 2 + 2 plots."""

    options_m10 = m10(options)
    variants = options_m10["variants"][:-2]

    options = default_options(variants, options)

    options["titles_columns"] = options_m10["titles_columns"]
    options["traits"] = options_m10["traits"][:-2]

    return options
