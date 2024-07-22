"""Single plot."""

from .default_data import default_data


def m01(data):
    """Single plot."""

    variants = [[f"{data['lang']}_noshuffle_cost15_4"]]

    default_data(data, variants)
