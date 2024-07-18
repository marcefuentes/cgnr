"""Figure 6."""

from .default_data import default_data
from .ss import S3, S5


def fig6(data):
    """Figure 6."""

    variants = [
        [
            "lang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "lang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
    ]

    data = default_data(data, variants)

    nrows = len(variants)

    data["givens_control"] = [["1.0", "1.0", "0.0", "0.0"] for _ in range(nrows)]
    data["mechanisms"] = [["pi", "pi", "pi", "pi"] for _ in range(nrows)]
    data["titles_columns"] = [S5, S3, "Production of $\\it{B}$", "Fitness"]
    data["traits"] = [
        ["Choose_ltGrainmean", "Imimic_ltGrainmean", "qBSeenmean", "wmean"]
        for _ in range(nrows)
    ]
    data["traits_control"] = data["traits"]

    return data
