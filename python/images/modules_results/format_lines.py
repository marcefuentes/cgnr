""" Format lines. """

import numpy as np


def format_lines(lines, params):
    """Format lines."""

    for idx in np.ndindex(lines.shape):
        line = lines[idx]
        line.set(**params)
