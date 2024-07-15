"""Many combinations of alphas and logess."""


def mxx(options):
    """Many combinations of alphas and logess."""

    _ = options  # To avoid unused variable warning.

    layout = {
        "alphas": {
            "start": 0.9,
            "stop": 0.1,
            "num": 3,
        },
        "logess": {
            "start": -2.0,
            "stop": 2.0,
            "num": 3,
        },
        "given_rows": [1.0, 0.99, 0.5, 0.0],
        "n_indifference_curves": 5,
        "budget_line": True,
    }

    return layout
