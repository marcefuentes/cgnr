"""Default options."""

from .repeat_for_matrix import repeat_for_matrix


def default_options(variants, options):
    """Default options."""

    nrows = len(variants)
    ncols = len(variants[0])

    titles = []
    for variant in variants[0]:
        if not variant:
            titles.append("")
        elif "noshuffle" in variant:
            titles.append("No shuffling")
        else:
            titles.append("Shuffling")

    options["givens"] = repeat_for_matrix(options["givens"], nrows, ncols)
    options["givens_control"] = repeat_for_matrix(
        options["givens_control"], nrows, ncols
    )
    options["mechanisms"] = repeat_for_matrix(options["mechanisms"], nrows, ncols)
    options["mechanisms_control"] = repeat_for_matrix(
        options["mechanisms_control"], nrows, ncols
    )
    options["titles_columns"] = titles
    options["titles_rows"] = [""] * nrows
    options["traits"] = repeat_for_matrix(options["traits"], nrows, ncols)
    options["traits_control"] = repeat_for_matrix(
        options["traits_control"], nrows, ncols
    )
    options["variants"] = variants
    options["variants_control"] = variants

    return options
