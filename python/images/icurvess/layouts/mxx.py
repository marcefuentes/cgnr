"""Many combinations of alphas and logess."""


def mxx(options):
    """Many combinations of alphas and logess."""

    options["alphas"] = {
        "start": 0.9,
        "stop": 0.1,
        "num": 3,
    }
    options["logess"] = {
        "start": -2.0,
        "stop": 2.0,
        "num": 3,
    }
    options["given_rows"] = [1.0, 0.99, 0.5, 0.0]
    options["n_indifference_curves"] = 5
    options["budget_line"] = True

    return options
