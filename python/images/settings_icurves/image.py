""" Parameters for the images module. """

import settings.image as common

PLOT_SIZE = common.PLOT_SIZE

image = {
    "colorbar_width": 0.025 * PLOT_SIZE,
    "margin_right": 0.5 * PLOT_SIZE,
    "margin_top": 0.3 * PLOT_SIZE,
    "budgets": {
        "alpha": 0.6,
        "color": "0.300",
        "linewidth": 0.9 * PLOT_SIZE,
    },
    "icurves": {
        "alpha": 0.8,
        "linewidth": 0.9 * PLOT_SIZE,
    },
    "icurves_grey": {
        "color": "0.850",
        "linewidth": 0.4 * PLOT_SIZE,
    },
    "landscapes": {
        "linewidth": 1.0 * PLOT_SIZE,
    },
}

image = {**common.image, **image}
