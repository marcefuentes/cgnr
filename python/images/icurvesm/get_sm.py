"""Create ScalarMappable object for color mapping."""

import numpy as np

from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import Normalize


def get_sm(color_map):
    """Create ScalarMappable object using the upper half of the color map."""

    color_array = color_map(np.linspace(0, 1, 256))
    new_map = ListedColormap(color_array[128:256])
    sm = ScalarMappable(cmap=new_map, norm=Normalize(0, 1))

    return sm
