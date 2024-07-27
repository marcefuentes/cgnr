"""Show how adding cooperation mechanisms contributes to aaleviating social dilemmas."""

from .default_data import default_data_ipi, get_subtitles


def fig7(data):
    """Plots for partner choice plus reciprocity."""

    mechanisms = ["p", "pi", "p", "pi"]
    variants_common = [
        f"nolang_noshuffle_cost15",
        f"lang_noshuffle_cost15",
        f"nolang_shuffle_cost15",
        f"lang_shuffle_cost15",
    ]
    default_data_ipi(data, mechanisms, variants_common)
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants_common, mechanisms
    )
