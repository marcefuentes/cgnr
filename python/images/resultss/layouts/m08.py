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

    data = default_data(variants, data)

    data["givens"] = [
        ["1.0", "1.0", "1.0"],
        ["1.0", "1.0", "1.0"],
        ["0.5", "0.5", "0.5"],
        ["0.5", "0.5", "0.5"],
    ]

    if data["givens_control"] != "0.0":
        data["givens_control"] = data["givens"]

    return data
