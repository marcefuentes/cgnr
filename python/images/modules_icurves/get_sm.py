"""Create ScalarMappable object for color mapping."""

import numpy as np

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from modules.settings import SETTINGS as settings


def get_sm():
    """Create ScalarMappable object using the upper half of the color map."""

    original_colors = cm.get_cmap(settings["color_map"], 256)
    color_array = original_colors(np.linspace(0, 1, 256))
    new_map = ListedColormap(color_array[128:256])
    sm = cm.ScalarMappable(cmap=new_map, norm=plt.Normalize(0, 1))

    return sm
