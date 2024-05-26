"""Create ScalarMappable object for color mapping."""

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt

from modules.settings import SETTINGS as settings


def get_sm():
    """Create ScalarMappable object for color mapping."""

    sm = ScalarMappable(cmap=settings["color_map"], norm=plt.Normalize(-1, 1))

    return sm
