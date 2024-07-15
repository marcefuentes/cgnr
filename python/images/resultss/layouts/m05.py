"""5 plots."""

from resultss.layouts.default_layout import default_layout
from resultss.layouts.ss import S1, S2, S3


def m05(options):
    """1 + 2 + 2 plots."""

    variants = [
        [
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
    ]

    layout = default_layout(variants, options)

    layout["titles_columns"] = [
        f"No shuffling\n{S1}, {S3}",
        f"Shuffling\n{S1}, {S2}",
        f"Shuffling\n{S1}, {S2}, {S3}",
    ]

    if options["trait"] == "ImimicGrainmean":
        for i in range(len(variants)):
            layout["traits"][i][0] = None
    elif options["trait"] == "Imimic_ltGrainmean":
        for i in range(len(variants)):
            layout["traits"][i][1] = None

    return layout
