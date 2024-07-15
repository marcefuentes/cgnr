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
        layout["traits"] = [[None, "ImimicGrainmean", "ImimicGrainmean"] for _ in range(len(variants))]
    elif options["trait"] == "Imimic_ltGrainmean":
        layout["traits"] = [["Imimic_ltGrainmean", None, "Imimic_ltGrainmean"] for _ in range(len(variants))]

    return layout
