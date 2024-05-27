""" Module to process the plot """

import matplotlib.pyplot as plt


def save_image(data_dict, file_name):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    if data_dict["update_function"] is not None:
        data_dict["update_function"](data_dict["frames"][-1], data_dict)
    plt.savefig(f"{file_name}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
