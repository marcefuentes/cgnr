"""Default data."""

from .repeat_for_matrix import repeat_for_matrix


def default_data(variants, data):
    """Default data."""

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

    data["givens"] = repeat_for_matrix(data["givens"], nrows, ncols)
    data["givens_control"] = repeat_for_matrix(data["givens_control"], nrows, ncols)
    data["mechanisms"] = repeat_for_matrix(data["mechanisms"], nrows, ncols)
    data["mechanisms_control"] = repeat_for_matrix(
        data["mechanisms_control"], nrows, ncols
    )
    data["titles_columns"] = titles
    data["titles_rows"] = [""] * nrows
    data["traits"] = repeat_for_matrix(data["traits"], nrows, ncols)
    data["traits_control"] = repeat_for_matrix(data["traits_control"], nrows, ncols)
    data["variants"] = variants
    data["variants_control"] = variants

    return data
