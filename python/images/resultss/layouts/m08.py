"""8 plots. """

from .default_data import default_data


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

    if data["traits"] == "qBSeenmean" or data["traits"] == "wmean":
        givens = repeat_for_matrix(data["givens"], nrows, ncols)
        givens_control = [
            [data["givens"] for _ in range(ncols)],
            [data["givens"] for _ in range(ncols)],
            ["0.0" for _ in range(ncols)],
            ["0.0" for _ in range(ncols)],
        ]
    else:
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

    data = default_data(variants, data)

    data["givens"] = givens
    data["givens_control"] = givens_control

    return data
