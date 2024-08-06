""" Process the figure and save """

import matplotlib.pyplot as plt


def save_image(data):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["text.usetex"] = True

    if data["function"] is not None:
        _ = data["function"](data["frames"][-1], data)
    plt.savefig(f"{data['file_name']}.png", transparent=False)
