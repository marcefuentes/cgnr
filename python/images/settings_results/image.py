""" Parameters for the images module. """

PLOT_SIZE = 4

image = {
    "big_label_size": 9 * PLOT_SIZE,
    "border_color": "0.3",
    "border_width": 0.1 * PLOT_SIZE,
    "bottom_margin": 0.625 * PLOT_SIZE,
    "color_map": "RdBu_r",
    "colorbar_height": PLOT_SIZE,
    "colorbar_right_position": 1,
    "colorbar_width": PLOT_SIZE / 21,
    "left_margin": 0.625 * PLOT_SIZE,
    "letter_label_size": 8 * PLOT_SIZE,
    "letter_padding": 0.035,
    "n_x_values": 64,
    "plot_size": PLOT_SIZE,
    "print_folder": False,
    "right_margin": 0.7 * PLOT_SIZE,
    "spacing": 0.1875 * PLOT_SIZE,
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
    "spines": {
        "color": "0.3",
        "linewidth": 0.1 * PLOT_SIZE,
    },
    "ticks": {
        "color": "0.3",
        "labelsize": 6 * PLOT_SIZE,
        "size": 2.0 * PLOT_SIZE,
    },
    "text_label_size": 8 * PLOT_SIZE,
    "title_padding": 11 * PLOT_SIZE,
    "top_margin": 0.625 * PLOT_SIZE,
    "x_label": "Substitutability of $\\it{B}$",
    "x_label_size": 0.5 * PLOT_SIZE,
    "y_label": "Influence of $\\it{B}$",
    "y_label_size": 0.5 * PLOT_SIZE,
}

image_lines = {
    "color": "0.4",
    "linewidth": 0.2 * PLOT_SIZE,
}

image_show = {
    "cmap": image["color_map"],
    "clim": (-1, 1),
}
