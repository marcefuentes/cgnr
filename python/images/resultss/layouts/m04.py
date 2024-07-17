"""3 plots."""

from .default_data import default_data


def m04(data):
    """4 plots."""

    lang = "lang" if data["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    data = default_data(data, variants)

    return data
