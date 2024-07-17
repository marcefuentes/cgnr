"""Single plot."""

from .default_data import default_data


def m01(data):
    """Single plot."""

    lang = "lang" if data["lang"] else "nolang"

    variants = [[f"{lang}_noshuffle_cost15_4"]]

    data = default_data(data, variants)

    return data
