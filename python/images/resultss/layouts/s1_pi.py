"""16 plots for reciprocity."""

from .default_data import default_data
from .repeat_for_matrix import repeat_for_matrix
from .ss import S1, S2, S3


def s1_pi(data):
    """1 + 1 + 2 + 2 + 2, twice."""

    mechanisms = ["pd", "pi", "pd", "pi", "pd", "pi", "pd", "pi"]
    variants_common = [
        "nolang_noshuffle_cost15",
        "nolang_noshuffle_cost15",
        "lang_noshuffle_cost15",
        "lang_noshuffle_cost15",
        "nolang_noshuffle_cost15",
        "nolang_noshuffle_cost15",
        "lang_noshuffle_cost15",
        "lang_noshuffle_cost15",
    ]

    suffixes = ["_128", "_4"]
    variants = []
    for _ in range(2):
        for suffix in suffixes:
            variants.append([f"{variant}{suffix}" for variant in variants_common])

    nrows = len(variants)
    ncols = len(variants_common)

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
    choose = False
    choose_lt = False
    if "imic" in data["traits"]:
        mimic = True
        if "mimic" in data["traits"]:
            imimic = True
            if "lt" in data["traits"]:
                imimic_lt = True
    if "Choose" in data["traits"]:
        choose = True
        if "lt" in data["traits"]:
            choose_lt = True

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = givens_control
    data["mechanisms"] = [mechanisms for _ in range(nrows)]

    for column, (variant, mechanism) in enumerate(zip(variants_common, mechanisms)):
        if "d" in mechanism:
            data["titles_columns"][column] += f"\n{S1}"
        if "i" in mechanism:
            data["titles_columns"][column] += f"\n{S1}"
            if "nolang" in variant:
                data["titles_columns"][column] += f", {S2}"
            else:
                if "_shuffle" in variant or "p" in mechanism:
                    data["titles_columns"][column] += f", {S2}"
                else:
                    imimic = False
                data["titles_columns"][column] += f", {S3}"
        if "p" in mechanism:
            data["titles_columns"][column] += f", {S4}"
            if variant.startswith("lang"):
                data["titles_columns"][column] += f", {S5}"
        if (
            (mimic and S1 not in data["titles_columns"][column])
            or (imimic and S2 not in data["titles_columns"][column])
            or (imimic_lt and S3 not in data["titles_columns"][column])
            or (choose and S4 not in data["titles_columns"][column])
            or (choose_lt and S5 not in data["titles_columns"][column])
        ):
            for i in range(nrows):
                data["traits"][i][column] = None

    return data
