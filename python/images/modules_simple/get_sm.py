"""Create ScalarMappable object for color mapping."""

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt


def get_sm(color_map):
    """Create ScalarMappable object for color mapping."""

    sm = ScalarMappable(cmap=color_map, norm=plt.Normalize(-1, 1))

    return sm
