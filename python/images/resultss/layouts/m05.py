"""Five plots."""

from resultsm.repeat_for_matrix import repeat_for_matrix
from resultss.layouts.ss import S1, S2, S3


def m05(options):
    """1 + 2 + 2 plots."""

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
    ]

    titles_columns = [
        f"No shuffling\n{S1}, {S3}",
        f"Shuffling\n{S1}, {S2}",
        f"Shuffling\n{S1}, {S2}, {S3}",
    ]

    if options["trait"] == "Imimic_ltGrainmean":
        traits = [
            [options["trait"], None, options["trait"]],
            [options["trait"], None, options["trait"]],
        ]
    elif options["trait"] == "ImimicGrainmean":
        traits = [
            [None, options["trait"], options["trait"]],
            [None, options["trait"], options["trait"]],
        ]
    else:
        traits = [
            [options["trait"], options["trait"], options["trait"]],
            [options["trait"], options["trait"], options["trait"]],
        ]

    nrows = len(variants)
    ncols = len(variants[0])

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": repeat_for_matrix(options["given_control"], nrows, ncols),
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": repeat_for_matrix(
            options["mechanism_control"], nrows, ncols
        ),
        "titles_columns": titles_columns,
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout
