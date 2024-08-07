"""2 plots."""

from resultsm.add_default_data import add_default_data


def m02(data):
    """2 plots."""

    variants = [
        [f"{data['lang']}_shuffle_cost15_128"],
        [f"{data['lang']}_shuffle_cost15_4"],
    ]

    add_default_data(data, variants)
