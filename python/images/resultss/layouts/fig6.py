"""Figure 6."""

from resultsm.add_default_data import add_default_data
from resultss.ss import S3, S5


def fig6(data):
    """Figure 6."""

    variants = [
        ["lang_shuffle_cost15_128" for _ in range(4)],
        ["lang_shuffle_cost15_4" for _ in range(4)],
    ]

    data["mechanisms"] = "pi"
    add_default_data(data, variants)

    data["givens_control"] = [["1.0", "1.0", "0.0", "0.0"] for _ in variants]
    data["titles_columns"] = [S5, S3, "Production of $\\it{B}$", "Fitness"]
    data["traits"] = data["traits_control"] = [
        ["Choose_ltGrainmean", "Imimic_ltGrainmean", "qBSeenmean", "wmean"]
        for _ in variants
    ]
