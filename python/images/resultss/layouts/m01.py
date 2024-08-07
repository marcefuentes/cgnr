"""Single plot."""

from resultsm.add_default_data import add_default_data


def m01(data):
    """Single plot."""

    variants = [[f"{data['lang']}_noshuffle_cost15_4"]]

    add_default_data(data, variants)
