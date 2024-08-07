"""Single combination of alphas and logess."""

from icurvesm.add_default_data import add_default_data


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

    if data["movie"]:
        data["frames_params"] = {
            "start": 0.0,
            "stop": 1.0,
            "num": 11,
        }

    add_default_data(data)
