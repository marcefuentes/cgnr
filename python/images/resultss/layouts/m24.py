"""24 plots for short-memory partner choice."""

from .default_data import default_data
from .repeat_for_matrix import repeat_for_matrix
from .ss import S1, S2, S3, S4, S5


def m24(data):
    """24 plots."""

    lang = "lang" if data["lang"] else "nolang"

    variants = [
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

    givens = [
        ["1.0" for _ in range(ncols)],
        ["1.0" for _ in range(ncols)],
        ["0.5" for _ in range(ncols)],
        ["0.5" for _ in range(ncols)],
    ]

    if data["givens_control"] == "0.0":
        givens_control = repeat_for_matrix("0.0", nrows, ncols)
    else:
        givens_control = givens

    mimic = False
    imimic = False
    imimic_lt = False
    if data["traits"] == "MimicGrainmean":
        mimic = True
    elif data["traits"] == "ImimicGrainmean":
        imimic = True
    elif data["traits"] == "Imimic_ltGrainmean":
        imimic_lt = True

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = givens_control
    data["mechanisms"] = [["p", "pd", "pi", "p", "pd", "pi"] for _ in range(nrows)]

    if data["lang"]:
        data["titles_columns"][0] += f"\n{S4}, {S5}"
        data["titles_columns"][1] += f"\n{S1}, {S4}, {S5}"
        data["titles_columns"][2] += f"\n{S1}, {S2}, {S3}, {S4}, {S5}"
        data["titles_columns"][3] += f"\n{S4}, {S5}"
        data["titles_columns"][4] += f"\n{S1}, {S4}, {S5}"
        data["titles_columns"][5] += f"\n{S1}, {S2}, {S3}, {S4}, {S5}"
    else:
        data["titles_columns"][0] += f"\n{S4}"
        data["titles_columns"][1] += f"\n{S1}, {S4}"
        data["titles_columns"][2] += f"\n{S1}, {S2}, {S4}"
        data["titles_columns"][3] += f"\n{S4}"
        data["titles_columns"][4] += f"\n{S1}, {S4}"
        data["titles_columns"][5] += f"\n{S1}, {S2}, {S4}"

    if imimic:
        for i in range(nrows):
            data["traits"][i][0] = None
            data["traits"][i][1] = None
            data["traits"][i][3] = None
            data["traits"][i][4] = None
    elif mimic:
        for i in range(nrows):
            data["traits"][i][0] = None
            data["traits"][i][3] = None

    return data
