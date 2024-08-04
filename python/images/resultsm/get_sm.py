"""Create ScalarMappable object for color mapping."""

from matplotlib.cm import ScalarMappable
from matplotlib.pyplot import Normalize


def get_sm(color_map):
    """Create ScalarMappable object for color mapping."""

    sm = ScalarMappable(cmap=color_map, norm=Normalize(-1, 1))

    return sm
