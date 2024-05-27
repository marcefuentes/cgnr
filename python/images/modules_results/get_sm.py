"""Create ScalarMappable object for color mapping."""

from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt

from settings_results.image import IMAGE as image

def get_sm():
    """Create ScalarMappable object for color mapping."""

    sm = ScalarMappable(cmap=image["color_map"], norm=plt.Normalize(-1, 1))

    return sm
