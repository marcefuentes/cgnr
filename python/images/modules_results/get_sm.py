"""Create ScalarMappable object for color mapping."""

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt

from modules.get_setting import get_setting as get


def get_sm():
    """Create ScalarMappable object for color mapping."""

    sm = ScalarMappable(cmap=get("COMMON", "color_map"), norm=plt.Normalize(-1, 1))

    return sm
