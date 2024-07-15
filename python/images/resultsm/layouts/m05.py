"""Five plots."""

from resultsm.repeat_for_matrix import repeat_for_matrix


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

    s1 = "$\\mathit{s}_{\\mathit{1}}$"
    s2 = "$\\mathit{s}_{\\mathit{2}}$"
    s3 = "$\\mathit{s}_{\\mathit{3}}$"

    titles_columns = [
        f"No shuffling\n{s1}, {s3}",
        f"Shuffling\n{s1}, {s2}",
        f"Shuffling\n{s1}, {s2}, {s3}",
    ]

    traits = [
        [options["trait"], None, options["trait"]],
        [options["trait"], None, options["trait"]],
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
