"""Plots for reciprocity."""

from .default_data import default_data_ipi, get_subtitles


def figi_adjust(data):
    """Plots for reciprocity."""

    mechanisms = ["d", "i", "d", "i", "i"]
    variants_common = [
        "nolang_noshuffle_cost15",
        "lang_noshuffle_cost15",
        "nolang_shuffle_cost15",
        "nolang_shuffle_cost15",
        "lang_shuffle_cost15",
    ]

    data = default_data_ipi(data, mechanisms, variants_common)
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants_common, mechanisms
    )

    return data
