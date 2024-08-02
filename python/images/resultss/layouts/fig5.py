"""Figure 5."""

from .default_data import default_data
from .ss import S1, S2


def fig5(data):
    """Figure 5."""

    variants = [
        ["nolang_shuffle_cost15_128" for _ in range(3)],
        ["nolang_shuffle_cost15_4" for _ in range(3)],
    ]

    data["givens_control"] = "1.0"
    data["mechanisms"] = "i"
    default_data(data, variants)

    data["titles_columns"] = [S1, S2, "Fitness"]
    data["traits"] = data["traits_control"] = [
        ["MimicGrainmean", "ImimicGrainmean", "wmean"] for _ in variants
    ]
