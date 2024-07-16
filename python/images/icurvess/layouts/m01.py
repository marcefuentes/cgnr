"""Single combination of alphas and logess."""


def m01(data):
    """Single combination of alphas and logess."""

    data["alphas_params"] = {
        "start": 0.5,
        "stop": 0.5,
        "num": 1,
    }
    data["logess_params"] = {
        "start": 0.0,
        "stop": 0.0,
        "num": 1,
    }
    data["givens"] = [0.0]
    data["n_indifference_curves"] = 5
    data["budget_line"] = True

    if data["movie"]:
        data["frames_params"] = {
            "start": 0.0,
            "stop": 1.0,
            "num": 11,
        }

    return data
