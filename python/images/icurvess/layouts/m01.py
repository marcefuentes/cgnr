"""Single combination of alphas and logess."""


def m01(options):
    """Single combination of alphas and logess."""

    options["alphas"] = {
        "start": 0.5,
        "stop": 0.5,
        "num": 1,
    }
    options["logess"] = {
        "start": 0.0,
        "stop": 0.0,
        "num": 1,
    }
    options["given_rows"] = [0.0]
    options["n_indifference_curves"] = 5
    options["budget_line"] = True

    if options["movie"]:
        options["movie_frames"] = {
            "start": 0.0,
            "stop": 1.0,
            "num": 11,
        }

    return options
