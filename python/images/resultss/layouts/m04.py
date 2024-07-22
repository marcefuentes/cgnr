"""4 plots."""

from .default_data import default_data, get_titles


def m04(data):
    """4 plots."""

    variants = [
        [f"{data['lang']}_noshuffle_cost15_128", f"{data['lang']}_shuffle_cost15_128"],
        [f"{data['lang']}_noshuffle_cost15_4", f"{data['lang']}_shuffle_cost15_4"],
    ]

    default_data(data, variants)
    data["titles_columns"] = get_titles(variants[0])
