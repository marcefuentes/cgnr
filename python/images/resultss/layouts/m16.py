"""16 plots."""

from resultss.layouts.default_options import default_options
from resultss.layouts.ss import S1, S2, S3, S4, S5


def m16(options):
    """All figures."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
    ]

    options = default_options(variants, options)

    if options["traits"] == "qBSeenmean" or options["traits"] == "wmean":
        options["givens_control"] = [
            [options["given"], options["given"], options["given"], options["given"]],
            [options["given"], options["given"], options["given"], options["given"]],
            ["0.0", "0.0", "0.0", "0.0"],
            ["0.0", "0.0", "0.0", "0.0"],
        ]
    else:
        options["givens"] = [
            ["1.0", "1.0", "1.0", "1.0"],
            ["1.0", "1.0", "1.0", "1.0"],
            ["0.5", "0.5", "0.5", "0.5"],
            ["0.5", "0.5", "0.5", "0.5"],
        ]

        if options["givens_control"] != "0.0":
            options["givens_control"] = options["givens"]

    options["mechanisms"] = [["pd", "pi", "pd", "pi"] for _ in range(len(variants))]

    if "Imimic" in options["traits"]:
        for i in range(len(variants)):
            options["traits"][i][0] = None
            options["traits"][i][2] = None

    if options["lang"]:
        options["titles_columns"][0] += f"\n{S1}, {S4}, {S5}"
        options["titles_columns"][1] += f"\n{S1}, {S2}, {S3}, {S4}, {S5}"
        options["titles_columns"][2] += f"\n{S1}, {S4}, {S5}"
        options["titles_columns"][3] += f"\n{S1}, {S2}, {S3}, {S4}, {S5}"
    else:
        options["titles_columns"][0] += f"\n{S1}, {S4}"
        options["titles_columns"][1] += f"\n{S1}, {S2}, {S4}"
        options["titles_columns"][2] += f"\n{S1}, {S4}"
        options["titles_columns"][3] += f"\n{S1}, {S2}, {S4}"

    return options
