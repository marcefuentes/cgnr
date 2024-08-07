"""Default data."""


def add_default_data(data):
    """Default data."""

    data["layout_i"] = len(data["givens"])
    data["layout_j"] = 2
    data["n_ic"] = 5
    data["budget_line"] = True

    data["titles_columns"] = ["", ""]
    data["titles_rows"] = [[""] for _ in data["givens"]]
