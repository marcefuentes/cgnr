""" Parameters for the images module. """

import settings.image as common

PLOT_SIZE = common.PLOT_SIZE
COLOR_MAP = common.COLOR_MAP

image = {
    "n_x_values": 64,
    "lines2d": {
        "color": "black",
        "linewidth": 0.3 * PLOT_SIZE,
    },
    "axesimage": {
        "cmap": COLOR_MAP,
        "clim": (-1, 1),
    },
}

image = {**common.image, **image}
