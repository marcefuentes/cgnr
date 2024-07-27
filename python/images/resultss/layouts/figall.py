"""Show how adding cooperation mechanisms contributes to aaleviating social dilemmas."""

from .default_data import default_data_ipi, get_subtitles


def figall(data):
    """Plots for partner choice plus reciprocity."""

    shuffle = "shuffle"
    mechanisms = ["p", "pd", "pi", "pd", "pi"]
    variants_common = [
        f"nolang_{shuffle}_cost15",
        f"nolang_{shuffle}_cost15",
        f"nolang_{shuffle}_cost15",
        f"lang_{shuffle}_cost15",
        f"lang_{shuffle}_cost15",
    ]
    default_data_ipi(data, mechanisms, variants_common)
    data["titles_columns"] = [""] * len(data["titles_columns"])
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants_common, mechanisms
    )
