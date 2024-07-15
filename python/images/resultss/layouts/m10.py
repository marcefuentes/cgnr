"""Ten plots."""

from resultsm.repeat_for_matrix import repeat_for_matrix
from resultss.layouts.ss import S1, S2, S3


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

    nrows = len(variants)
    ncols = len(variants[0])

    givens = [
        ["1.0", "1.0", "1.0"],
        ["1.0", "1.0", "1.0"],
        ["0.5", "0.5", "0.5"],
        ["0.5", "0.5", "0.5"],
    ]

    givens_control = givens
    givens_control = repeat_for_matrix("0.0", nrows, ncols)

    mechanisms = repeat_for_matrix("i", nrows, ncols)

    if options["trait"] == "ImimicGrainmean":
        traits = [[None, options["trait"], options["trait"]] for _ in range(nrows)]
    elif options["trait"] == "Imimic_ltGrainmean":
        traits = [[options["trait"], None, options["trait"]] for _ in range(nrows)]
    else:
        traits = repeat_for_matrix(options["trait"], nrows, ncols)

    titles_columns = [
        f"No shuffling\n{S1}, {S3}",
        f"Shuffling\n{S1}, {S2}",
        f"Shuffling\n{S1}, {S2}, {S3}",
    ]

    layout = {
        "givens": givens,
        "givens_control": givens_control,
        "mechanisms": mechanisms,
        "mechanisms_control": repeat_for_matrix("none", nrows, ncols),
        "titles_columns": titles_columns,
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout
