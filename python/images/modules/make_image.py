""" Module to process the plot """

import matplotlib.pyplot as plt


def make_image(frames, kwargs, name):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    kwargs["update_function"](frames[-1], kwargs)
    plt.savefig(f"{name}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
