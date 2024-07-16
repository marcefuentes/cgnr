"""16 plots."""

from .default_data import default_data
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

    data = default_data(variants, data)

    if data["givens_control"] != "0.0":
        data["givens_control"] = [
            ["1.0", "1.0", "1.0", "1.0", "1.0"],
            ["1.0", "1.0", "1.0", "1.0", "1.0"],
            ["0.5", "0.5", "0.5", "0.5", "0.5"],
            ["0.5", "0.5", "0.5", "0.5", "0.5"],
        ]

    data["mechanisms"] = [["d", "i", "d", "i", "i"] for _ in range(len(variants))]

    data["titles_columns"][0] += f"\n{S1}"
    data["titles_columns"][1] += f"\n{S1}, {S3}"
    data["titles_columns"][2] += f"\n{S1}"
    data["titles_columns"][3] += f"\n{S1}, {S2}"
    data["titles_columns"][4] += f"\n{S1}, {S2}, {S3}"

    if data["traits"] == "ImimicGrainmean":
        for i in range(len(variants)):
            data["traits"][i][0] = None
            data["traits"][i][1] = None
            data["traits"][i][2] = None
    elif data["traits"] == "Imimic_ltGrainmean":
        for i in range(len(variants)):
            data["traits"][i][0] = None
            data["traits"][i][2] = None
            data["traits"][i][3] = None

    return data
