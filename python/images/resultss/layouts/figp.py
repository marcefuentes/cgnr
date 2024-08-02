"""8 plots. """

from resultsm.default_data import default_data_ipi


def figp(data):
    """4 given=1.0. 4 given=0.5."""

    mechanisms = ["p", "p"]
    variants_common = [
        f"{data['lang']}_noshuffle_cost15",
        f"{data['lang']}_shuffle_cost15",
    ]

    default_data_ipi(data, mechanisms, variants_common)
