"""Many combinations of alphas and logess."""

from icurvesm.add_default_data import add_default_data


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

    add_default_data(data)
