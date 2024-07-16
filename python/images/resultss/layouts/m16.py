"""16 plots."""

from .default_data import default_data
from .repeat_for_matrix import repeat_for_matrix
from .ss import S1, S2, S3, S4, S5


def m16(data):
    """16 plots."""

    lang = "lang" if data["lang"] else "nolang"

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

    nrows = len(variants)
    ncols = len(variants[0])

    if data["traits"] == "qBSeenmean" or data["traits"] == "wmean":
        givens = repeat_for_matrix(data["givens"], nrows, ncols)
        givens_control = [
            [data["givens"], data["givens"], data["givens"], data["givens"]],
            [data["givens"], data["givens"], data["givens"], data["givens"]],
            ["0.0", "0.0", "0.0", "0.0"],
            ["0.0", "0.0", "0.0", "0.0"],
        ]
    else:
        givens = [
            ["1.0", "1.0", "1.0", "1.0"],
            ["1.0", "1.0", "1.0", "1.0"],
            ["0.5", "0.5", "0.5", "0.5"],
            ["0.5", "0.5", "0.5", "0.5"],
        ]

        if data["givens_control"] == "0.0":
            givens_control = repeat_for_matrix("0.0", nrows, ncols)
        else:
            givens_control = givens

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = givens_control
    data["mechanisms"] = [["pd", "pi", "pd", "pi"] for _ in range(len(variants))]
    if data["lang"]:
        data["titles_columns"][0] += f"\n{S1}, {S4}, {S5}"
        data["titles_columns"][1] += f"\n{S1}, {S2}, {S3}, {S4}, {S5}"
        data["titles_columns"][2] += f"\n{S1}, {S4}, {S5}"
        data["titles_columns"][3] += f"\n{S1}, {S2}, {S3}, {S4}, {S5}"
    else:
        data["titles_columns"][0] += f"\n{S1}, {S4}"
        data["titles_columns"][1] += f"\n{S1}, {S2}, {S4}"
        data["titles_columns"][2] += f"\n{S1}, {S4}"
        data["titles_columns"][3] += f"\n{S1}, {S2}, {S4}"


    if "Imimic" in data["traits"]:
        for i in range(len(variants)):
            data["traits"][i][0] = None
            data["traits"][i][2] = None

    return data
