""" Parameters for the images module. """

COLOR_MAP = "RdBu_r"
PLOT_SIZE = 4

image = {
    "bottom_margin": 0.625 * PLOT_SIZE,
    "color_map": COLOR_MAP,
    "colorbar_height": PLOT_SIZE,
    "colorbar_right_position": 1,
    "colorbar_width": 0.025 * PLOT_SIZE,
    "left_margin": 0.625 * PLOT_SIZE,
    "letter_padding": 0.035,
    "plot_size": PLOT_SIZE,
    "print_folder": False,
    "right_margin": 0.5 * PLOT_SIZE,
    "spacing": 0.1875 * PLOT_SIZE,
    "suplabel_size": 9 * PLOT_SIZE,
    "title_padding": 11 * PLOT_SIZE,
    "top_margin": 0.3 * PLOT_SIZE,
    "x_label": "Substitutability of $\\it{B}$",
    "x_label_size": 0.5 * PLOT_SIZE,
    "y_label": "Influence of $\\it{B}$",
    "y_label_size": 0.5 * PLOT_SIZE,

    "budgets": {
        "alpha": 0.6,
        "color": "0.300",
        "linewidth": 0.9 * PLOT_SIZE,
    },
    "colorbar": {
        "edgecolor": "0.3",
        "linewidth": 0.1 * PLOT_SIZE,
    },
    "column_titles": {
        "fontsize": 8 * PLOT_SIZE,
        "pad": 11 * PLOT_SIZE,
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
    "letters": {
        "fontsize": 8 * PLOT_SIZE,
        "weight": "bold",
    },
    "row_titles": {
        "fontsize": 8 * PLOT_SIZE,
        "ha": "left",
        "textcoords": "offset points",
        "va": "center",
        "xy": (1, 0.5),
        "xycoords": "axes fraction",
        "xytext": (11 * 3.5 * PLOT_SIZE, 0),
    },
    "show": {
        "cmap": COLOR_MAP,
        "clim": (-1, 1),
    },
    "spines": {
        "color": "0.3",
        "linewidth": 0.1 * PLOT_SIZE,
    },
    "text": {
        "color": "0.3",
        "fontsize": 8 * PLOT_SIZE,
    },
    "ticks": {
        "color": "0.3",
        "labelsize": 6 * PLOT_SIZE,
        "size": 0 * PLOT_SIZE,
    },
}
