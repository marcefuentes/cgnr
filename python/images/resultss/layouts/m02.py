"""Two plots."""

from .default_data import default_data


def m02(data):
    """Two plots."""

    lang = "lang" if data["lang"] else "nolang"

    variants = [
        [f"{lang}_shuffle_cost15_128"],
        [f"{lang}_shuffle_cost15_4"],
    ]

    data = default_data(data, variants)

    return data
