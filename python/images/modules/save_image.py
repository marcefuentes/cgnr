""" Module to process the plot """

import matplotlib.pyplot as plt


def save_image(update_args):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    update_args["update_function"](update_args["frames"][-1], update_args)
    plt.savefig(f"{update_args['file_name']}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
