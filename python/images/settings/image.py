""" Parameters for the images module. """

COLOR_MAP = "RdBu_r"
GREY = "0.7"
LINE_WIDTH = 0.2
PLOT_SIZE = 4

image = {
    "color_map": COLOR_MAP,
    "colorbar_height": PLOT_SIZE,
    "colorbar_position_right": 1,
    "colorbar_width": PLOT_SIZE / 21,
    "margin_bottom": 0.625 * PLOT_SIZE,
    "margin_inner": 0.1875 * PLOT_SIZE,
    "margin_left": 0.625 * PLOT_SIZE,
    "margin_right": 0.7 * PLOT_SIZE,
    "margin_top": 0.625 * PLOT_SIZE,
    "padding_letter": 0.035,
    "padding_title": 11 * PLOT_SIZE,
    "plot_size": PLOT_SIZE,
    "print_folder": False,
    "suplabel_size": 9 * PLOT_SIZE,
    "suplabel_x": "Substitutability of $\\it{B}$",
    "suplabel_y": "Influence of $\\it{B}$",
    "colorbar": {
        "edgecolor": GREY,
        "linewidth": LINE_WIDTH * PLOT_SIZE,
    },
    "spines": {
        "color": GREY,
        "linewidth": LINE_WIDTH * PLOT_SIZE,
    },
    "ticks": {
        "color": GREY,
        "labelsize": 6 * PLOT_SIZE,
        "length": 1.0 * PLOT_SIZE,
        "width": LINE_WIDTH * PLOT_SIZE,
    },
    "column_titles": {
        "fontsize": 8 * PLOT_SIZE,
        "pad": 11 * PLOT_SIZE,
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
    "text": {
        "color": "0.3",
        "fontsize": 8 * PLOT_SIZE,
    },
}
