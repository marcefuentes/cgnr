"""10 plots."""

from .default_options import default_options
from .ss import S1, S2, S3


def m10(options):
    """1 + 2 + 2 plots, twice."""

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

    options = default_options(variants, options)

    if options["givens_control"][0][0] != "0.0":
        options["givens_control"] = [
            ["1.0", "1.0", "1.0"],
            ["1.0", "1.0", "1.0"],
            ["0.5", "0.5", "0.5"],
            ["0.5", "0.5", "0.5"],
        ]

    options["titles_columns"][0] += f"\n{S1}, {S3}"
    options["titles_columns"][1] += f"\n{S1}, {S2}"
    options["titles_columns"][2] += f"\n{S1}, {S2}, {S3}"

    if options["traits"] == "ImimicGrainmean":
        for i in range(len(variants)):
            options["traits"][i][0] = None
    elif options["traits"] == "Imimic_ltGrainmean":
        for i in range(len(variants)):
            options["traits"][i][1] = None

    return options
