"""8 plots. """

from .default_data import default_data, get_givens, get_titles


def m08(data):
    """4 given=1.0. 4 given=0.5."""

    lang = "lang" if data["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

    givens, givens_control = get_givens(data["givens_control"], nrows, ncols)
    data = default_data(data, variants)
    data["givens"] = givens
    data["givens_control"] = givens_control
    data["titles_columns"] = get_titles(variants)

    return data
