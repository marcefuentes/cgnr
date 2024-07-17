"""Figure 5."""

from .default_data import default_data
from .ss import S1, S2

def fig5(data):
    """Figure 5."""

    variants = [
        [f"nolang_shuffle_cost15_128", f"nolang_shuffle_cost15_128", f"nolang_shuffle_cost15_128"],
        [f"nolang_shuffle_cost15_4", f"nolang_shuffle_cost15_4", f"nolang_shuffle_cost15_4"],
    ]

    nrows = len(variants)

    data = default_data(data, variants)

    data["givens_control"] = [["1.0", "1.0", "1.0"] for _ in range(nrows)]
    data["mechanisms"] = [["i", "i", "i"] for _ in range(nrows)]
    data["titles_columns"] = [S1, S2, "Fitness"]
    data["traits"] = [["MimicGrainmean", "ImimicGrainmean", "wmean"] for _ in range(nrows)]
    data["traits_control"] = data["traits"]

    return data
