""" Parameters for the images module. """

import settings.image as common

PLOT_SIZE = common.PLOT_SIZE

image = {
    "n_x_values": 64,
    "lines": {
        "color": "0.4",
        "linewidth": 0.2 * PLOT_SIZE,
    },
    "show": {
        "cmap": COLOR_MAP,
        "clim": (-1, 1),
    },
}

image = {**common.image, **image}
