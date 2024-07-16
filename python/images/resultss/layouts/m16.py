"""16 plots."""

from .default_data import default_data
from .ss import S1, S2, S3, S4, S5


def m16(data):
    """All figures."""

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

    data = default_data(variants, data)

    if data["traits"] == "qBSeenmean" or data["traits"] == "wmean":
        data["givens_control"] = [
            [data["given"], data["given"], data["given"], data["given"]],
            [data["given"], data["given"], data["given"], data["given"]],
            ["0.0", "0.0", "0.0", "0.0"],
            ["0.0", "0.0", "0.0", "0.0"],
        ]
    else:
        data["givens"] = [
            ["1.0", "1.0", "1.0", "1.0"],
            ["1.0", "1.0", "1.0", "1.0"],
            ["0.5", "0.5", "0.5", "0.5"],
            ["0.5", "0.5", "0.5", "0.5"],
        ]

        if data["givens_control"] != "0.0":
            data["givens_control"] = data["givens"]

    data["mechanisms"] = [["pd", "pi", "pd", "pi"] for _ in range(len(variants))]

    if "Imimic" in data["traits"]:
        for i in range(len(variants)):
            data["traits"][i][0] = None
            data["traits"][i][2] = None

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

    return data
