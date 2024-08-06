"""Many combinations of alphas and logess."""


def mxx(data):
    """Many combinations of alphas and logess."""

    data["alphas_params"] = {
        "start": 0.9,
        "stop": 0.1,
        "num": 3,
    }
    data["logess_params"] = {
        "start": -2.0,
        "stop": 2.0,
        "num": 3,
    }
    data["givens"] = [1.0, 0.99, 0.5, 0.0]
    data["layout_i"] = len(data["givens"])
    data["layout_j"] = 2
    data["n_ic"] = 5
    data["budget_line"] = True

    data["titles_columns"] = ["", ""]
    data["titles_rows"] = [[""] for _ in data["givens"]]
