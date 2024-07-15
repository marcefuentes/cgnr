"""16 plots for qBSeenmean or wmean."""

from resultsm.repeat_for_matrix import repeat_for_matrix
from resultss.layouts.ss import S1, S2, S3, S4, S5


def m16qbw(options):
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

    nrows = len(variants)
    ncols = len(variants[0])

    givens_control = [
        [options["given"], options["given"], options["given"], options["given"]],
        [options["given"], options["given"], options["given"], options["given"]],
        ["0.0", "0.0", "0.0", "0.0"],
        ["0.0", "0.0", "0.0", "0.0"],
    ]

    mechanisms = [["pd", "pi", "pd", "pi"] for _ in range(nrows)]

    if "Imimic" in options["trait"]:
        traits = [
            [None, options["trait"], None, options["trait"]] for _ in range(nrows)
        ]
    else:
        traits = repeat_for_matrix(options["trait"], nrows, ncols)

    titles_columns = [
        f"No shuffling\n{S1}, {S4}",
        f"No shuffling\n{S1}, {S2}, {S4}",
        f"Shuffling\n{S1}, {S4}",
        f"Shuffling\n{S1}, {S2}, {S4}",
    ]

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
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
