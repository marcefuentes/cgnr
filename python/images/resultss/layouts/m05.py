"""5 plots."""

from resultss.layouts.default_layout import default_layout
from resultss.layouts.m10 import m10
from resultss.layouts.ss import S1, S2, S3


def m05(options):
    """1 + 2 + 2 plots."""

    layout_m10 = m10(options)
    variants = layout_m10["variants"][:-2]

    layout = default_layout(variants, options)

    layout["titles_columns"] = layout_m10["titles_columns"]
    layout["traits"] = layout_m10["traits"][:-2]

    return layout
