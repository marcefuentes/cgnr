""" Process the figure and save """

import matplotlib.pyplot as plt


def save_image(update_args, config_data, dynamic_data):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    if update_args["function"] is not None:
        update_args["function"](dynamic_data["frames"][-1], update_args["artists"], config_data, dynamic_data)
    plt.savefig(f"{update_args['file_name']}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
