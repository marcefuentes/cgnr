"""8 plots. """

from .default_data import default_data_ipi


def figp(data):
    """4 given=1.0. 4 given=0.5."""

    lang = "lang" if data["lang"] else "nolang"
    mechanisms = ["p", "p"]
    variants_common = [
        f"{lang}_noshuffle_cost15",
        f"{lang}_shuffle_cost15",
    ]

    data = default_data_ipi(data, mechanisms, variants_common)

    return data
