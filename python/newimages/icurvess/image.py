""" Parameters for the images module. """

import settings.image as project

PLOT_SIZE = project.PLOT_SIZE

image_common = {
    "colorbar_width": 0.025 * PLOT_SIZE,
    "margin_right": 0.5 * PLOT_SIZE,
    "margin_top": 0.3 * PLOT_SIZE,
    "n_x_values": 64,
    "budgets": {
        "alpha": 0.6,
        "color": "0.300",
        "linewidth": 1.8 * PLOT_SIZE,
    },
    "icurves": {
        "alpha": 0.8,
        "linewidth": 1.8 * PLOT_SIZE,
    },
    "icurves_grey": {
        "color": "0.850",
        "linewidth": 0.8 * PLOT_SIZE,
    },
    "landscapes": {
        "linewidth": 2.0 * PLOT_SIZE,
    },
}

image_common = {**project.image, **image_common}


image_unit = {
    "colorbar_position_right": 0.35,
    "labelpad": 4 * PLOT_SIZE,
    "margin_right": 0.6 * PLOT_SIZE,
    "margin_inner": 0.6 * PLOT_SIZE,
    "suplabel_x": "",
    "suplabel_y": "",
    "label_x_0": "$\\mathit{c}_{\\mathit{A}}$",
    "label_x_1": "$\\mathit{q}_{\\mathit{B}}$",
    "label_y_0": "$\\mathit{c}_{\\mathit{B}}$",
    "label_y_1": "$\\mathit{w}$",
}

image_unit = {**image_common, **image_unit}

image_unit["ticks"]["labelsize"] *= 0.8
