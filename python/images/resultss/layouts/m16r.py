"""16 plots."""

from resultss.layouts.default_layout import default_layout
from resultss.layouts.ss import S1, S2, S3


def m16r(options):
    """1 + 1 + 2 + 2 + 2, twice."""

    variants = [
        [
            "nolang_noshuffle_cost15_128",
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "nolang_noshuffle_cost15_4",
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
        [
            "nolang_noshuffle_cost15_128",
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "nolang_noshuffle_cost15_4",
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
    ]

    layout = default_layout(variants, options)

    if options["given_control"] != "0.0":
        layout["givens_control"] = [
            ["1.0", "1.0", "1.0", "1.0", "1.0"],
            ["1.0", "1.0", "1.0", "1.0", "1.0"],
            ["0.5", "0.5", "0.5", "0.5", "0.5"],
            ["0.5", "0.5", "0.5", "0.5", "0.5"],
        ]

    layout["mechanisms"] = [["d", "i", "d", "i", "i"] for _ in range(len(variants))]

    layout["titles_columns"][0] += f"\n{S1}"
    layout["titles_columns"][1] += f"\n{S1}, {S3}"
    layout["titles_columns"][2] += f"\n{S1}"
    layout["titles_columns"][3] += f"\n{S1}, {S2}"
    layout["titles_columns"][4] += f"\n{S1}, {S2}, {S3}"

    if options["trait"] == "ImimicGrainmean":
        for i in range(len(variants)):
            layout["traits"][i][0] = None
            layout["traits"][i][1] = None
            layout["traits"][i][2] = None
    elif options["trait"] == "Imimic_ltGrainmean":
        for i in range(len(variants)):
            layout["traits"][i][0] = None
            layout["traits"][i][2] = None
            layout["traits"][i][3] = None

    return layout
