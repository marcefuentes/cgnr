"""Plots for partner choice plus reciprocity."""

from .default_data import default_data_subtitles, get_subtitles


def s1_pi(data):
    """Plots for partner choice plus reciprocity."""

    lang = "lang" if data["lang"] else "nolang"
    mechanisms = ["pd", "pi", "pd", "pi"]
    variants_common = [
        f"{lang}_noshuffle_cost15",
        f"{lang}_noshuffle_cost15",
        f"{lang}_shuffle_cost15",
        f"{lang}_shuffle_cost15",
    ]

    data = default_data_subtitles(data, mechanisms, variants_common)
    data["titles_columns"] = get_subtitles(data["titles_columns"], variants_common, mechanisms)

    return data
