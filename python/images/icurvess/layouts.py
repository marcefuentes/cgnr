""" Layouts for icurves. """

def all3(options):
    """Data common to all subplots."""

    _ = options # To avoid unused variable warning.

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


def all21(options):
    """Data common to all subplots."""

    _ = options # To avoid unused variable warning.

    layout = {
        "alphas": {
            "start": 0.9,
            "stop": 0.1,
            "num": 21,
        },
        "logess": {
            "start": -5.0,
            "stop": 5.0,
            "num": 21,
        },
        "given_rows": [1.0, 0.99, 0.5, 0.0],
        "n_indifference_curves": 5,
        "budget_line": False,
    }

    return layout


def onerow(options):
    """Data common to all subplots."""

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


def unit(options):
    """Data common to all subplots."""

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
