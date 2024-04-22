""" Module to process the plot """

import matplotlib.pyplot as plt
from modules_results.update import update_artists


def make_image(fig, frames, update_data, name):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    update_artists(frames[-1], update_data)
    plt.savefig(f"{name}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
