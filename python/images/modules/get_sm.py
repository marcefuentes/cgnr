"""Create ScalarMappable object for color mapping."""

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt

from modules.settings import COLOR_MAP

def get_sm():
    """Create ScalarMappable object for color mapping."""

    sm = ScalarMappable(cmap=COLOR_MAP, norm=plt.Normalize(-1, 1))

    return sm
