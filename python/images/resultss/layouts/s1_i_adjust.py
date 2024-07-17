"""Plots for reciprocity."""

from .default_data import default_data_subtitles
from .repeat_for_matrix import repeat_for_matrix


def s1_i_adjust(data):
    """Plots for reciprocity."""

    mechanisms = ["d", "i", "d", "i", "i"]
    variants_common = [
        "nolang_noshuffle_cost15",
        "lang_noshuffle_cost15",
        "nolang_shuffle_cost15",
        "nolang_shuffle_cost15",
        "lang_shuffle_cost15",
    ]

    data = default_data_subtitles(data, mechanisms, variants_common)

    return data
