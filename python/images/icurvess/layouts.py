""" Layouts for icurves. """

def layouts():
    """Data common to all subplots."""

    layout = {
        "given_frames": {
            "start": 0.0,
            "stop": 1.0,
            "num": 11,
        },
        "alphas": {
            "start": 0.1,
            "stop": 0.9,
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
