"""Show how adding cooperation mechanisms contributes to aaleviating social dilemmas."""

from .default_data import default_data, get_subtitles


def fig7(data):
    """Plots for partner choice plus reciprocity."""

    mechanisms = ["p", "pi", "p", "pi"]
    variants = [
        [
            "nolang_noshuffle_cost15_128",
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "nolang_noshuffle_cost15_4",
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
    ]
    default_data(data, variants)
    data["mechanisms"] = [mechanisms for _ in range(len(variants))]
    data["titles_columns"] = ["No shuffling", "No shuffling", "Shuffling", "Shuffling"]
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants[0], mechanisms
    )
