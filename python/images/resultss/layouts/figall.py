"""Show how adding cooperation mechanisms contributes to aaleviating social dilemmas."""

from resultsm.add_default_data import add_default_data_ipi, get_subtitles


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
    add_default_data_ipi(data, mechanisms, variants_common)
    data["titles_columns"] = [""] * data["layout_j"]
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants_common, mechanisms
    )
