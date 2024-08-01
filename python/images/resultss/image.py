""" Parameters for the images module. """

import settings.image as common

PLOT_SIZE = common.PLOT_SIZE
COLOR_MAP = common.COLOR_MAP

image = {
    "n_x_values": 64,
    "AxesImage": {
        "cmap": COLOR_MAP,
        "clim": (-1, 1),
    },
    "Line2D": {
        "color": "brown",
        "linewidth": 0.00001 * PLOT_SIZE,
    },
    "PolyCollection": {
        "color": "brown",
        "linewidth": 0.00001 * PLOT_SIZE,
    },
}

image = {**common.image, **image}
