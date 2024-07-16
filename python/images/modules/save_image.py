""" Process the figure and save """

import matplotlib.pyplot as plt


def save_image(data, options):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["text.usetex"] = True

    if data["function"] is not None:
        _ = data["function"](data["frames"][-1], data, options)
    plt.savefig(f"{data['file_name']}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
