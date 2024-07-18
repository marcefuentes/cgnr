"""Plots for partner choice plus reciprocity."""

from .default_data import default_data_ipi, get_subtitles


def figpi(data):
    """Plots for partner choice plus reciprocity."""

    mechanisms = ["pd", "pi", "pd", "pi"]
    lang = "lang" if data["lang"] else "nolang"
    variants_common = [
        f"{lang}_noshuffle_cost15",
        f"{lang}_noshuffle_cost15",
        f"{lang}_shuffle_cost15",
        f"{lang}_shuffle_cost15",
    ]

    data = default_data_ipi(data, mechanisms, variants_common)
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants_common, mechanisms
    )

    return data
