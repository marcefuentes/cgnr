"""Default layout."""

from resultsm.repeat_for_matrix import repeat_for_matrix


def default_layout(variants, options):
    """Default layout."""

    nrows = len(variants)
    ncols = len(variants[0])

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": repeat_for_matrix(options["given_control"], nrows, ncols),
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": repeat_for_matrix(
            options["mechanism_control"], nrows, ncols
        ),
        "titles_columns": [""] * ncols,
        "titles_rows": [""] * nrows,
        "traits": repeat_for_matrix(options["trait"], nrows, ncols),
        "traits_control": repeat_for_matrix(options["trait_control"], nrows, ncols),
        "variants": variants,
        "variants_control": variants,
    }

    return layout
