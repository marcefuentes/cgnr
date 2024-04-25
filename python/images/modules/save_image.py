""" Module to process the plot """

import matplotlib.pyplot as plt


def save_image(frame, update_args, name):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    update_args["update_function"](frame, update_args)
    plt.savefig(f"{name}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
