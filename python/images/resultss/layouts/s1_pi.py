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

    imimic = False
    imimic_lt = False
    if data["traits"] == "ImimicGrainmean":
        imimic = True
    elif data["traits"] == "Imimic_ltGrainmean":
        imimic_lt = True

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = givens_control
    data["mechanisms"] = [mechanisms for _ in range(nrows)]

    for column, (variant, mechanism) in enumerate(zip(variants_common, mechanisms)):
        data["titles_columns"][column] += f"\n{S1}"
        if "i" in mechanism:
            if "nolang" in variant:
                data["titles_columns"][column] += f", {S2}"
                if imimic_lt:
                    for i in range(nrows):
                        data["traits"][i][column] = None
            else:
                if "_shuffle" in variant or "p" in mechanism:
                    data["titles_columns"][column] += f", {S2}"
                else:
                    if imimic:
                        for i in range(nrows):
                            data["traits"][i][column] = None
                data["titles_columns"][column] += f", {S3}"

    return data
