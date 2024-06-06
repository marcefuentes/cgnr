""" Format lines. """

import numpy as np


def format_lines(lines, image):
    """Format lines."""

    for idx in np.ndindex(lines.shape):
        line = lines[idx]
        line.set_color(image["line_color"])
        line.set_linewidth(image["line_width"] * image["plot_size"])
