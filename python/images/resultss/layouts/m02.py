"""2 plots."""

from .default_data import default_data


def m02(data):
    """2 plots."""

    variants = [
        [f"{data['lang']}_shuffle_cost15_128"],
        [f"{data['lang']}_shuffle_cost15_4"],
    ]

    default_data(data, variants)
