"""Single combination of alphas and logess."""


def m01(options):
    """Single combination of alphas and logess."""

    layout = {
        "alphas": {
            "start": 0.5,
            "stop": 0.5,
            "num": 1,
        },
        "logess": {
            "start": 0.0,
            "stop": 0.0,
            "num": 1,
        },
        "given_rows": [0.0],
        "n_indifference_curves": 5,
        "budget_line": True,
    }

    if options["movie"]:
        layout["movie_frames"] = {
            "start": 0.0,
            "stop": 1.0,
            "num": 11,
        }

    return layout
