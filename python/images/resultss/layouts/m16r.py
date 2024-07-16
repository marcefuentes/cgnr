"""16 plots for reciprocity."""

from .default_data import default_data
from .repeat_for_matrix import repeat_for_matrix
from .ss import S1, S2, S3


def m16r(data):
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

    imimic = False
    imimic_lt = False
    if data["traits"] == "ImimicGrainmean":
        imimic = True
    elif data["traits"] == "Imimic_ltGrainmean":
        imimic_lt = True

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = givens_control
    data["mechanisms"] = [["d", "i", "d", "i", "i"] for _ in range(nrows)]

    data["titles_columns"][0] += f"\n{S1}"
    data["titles_columns"][1] += f"\n{S1}, {S3}"
    data["titles_columns"][2] += f"\n{S1}"
    data["titles_columns"][3] += f"\n{S1}, {S2}"
    data["titles_columns"][4] += f"\n{S1}, {S2}, {S3}"

    if imimic:
        for i in range(nrows):
            data["traits"][i][0] = None
            data["traits"][i][1] = None
            data["traits"][i][2] = None
    elif imimic_lt:
        for i in range(nrows):
            data["traits"][i][0] = None
            data["traits"][i][2] = None
            data["traits"][i][3] = None

    return data
