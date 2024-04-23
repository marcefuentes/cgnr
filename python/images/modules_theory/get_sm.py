"""Create ScalarMappable object for color mapping."""

import numpy as np

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from modules.settings import COLOR_MAP


def get_sm():
    """Create ScalarMappable object using the upper half of the color map."""

    RdBu_r = cm.get_cmap(COLOR_MAP, 256)
    newcolors = RdBu_r(np.linspace(0, 1, 256))
    new_map = ListedColormap(newcolors[128:256])
    sm = cm.ScalarMappable(cmap=new_map, norm=plt.Normalize(0, 1))

    return sm
