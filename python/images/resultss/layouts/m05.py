"""5 plots."""

from resultss.layouts.default_options import default_options
from resultss.layouts.m10 import m10


def m05(options):
    """1 + 2 + 2 plots."""

    options_m10 = m10(options)

    options["givens"] = options_m10["givens"][:-2]
    options["givens_control"] = options_m10["givens_control"][:-2]
    options["mechanisms"] = options_m10["mechanisms"][:-2]
    options["mechanisms_control"] = options_m10["mechanisms_control"][:-2]
    options["titles_columns"] = options_m10["titles_columns"]
    options["titles_rows"] = options_m10["titles_rows"][:-2]
    options["traits"] = options_m10["traits"][:-2]
    options["traits_control"] = options_m10["traits_control"][:-2]
    options["variants"] = options_m10["variants"][:-2]
    options["variants_control"] = options_m10["variants_control"][:-2]

    return options
