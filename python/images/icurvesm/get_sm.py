"""Create ScalarMappable object for color mapping."""

import numpy as np

from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


def get_sm(color_map):
    """Create ScalarMappable object using the upper half of the color map."""

    original_colors = plt.get_cmap(color_map, 256)
    color_array = original_colors(np.linspace(0, 1, 256))
    new_map = ListedColormap(color_array[128:256])
    sm = cm.ScalarMappable(cmap=new_map, norm=plt.Normalize(0, 1))

    return sm
