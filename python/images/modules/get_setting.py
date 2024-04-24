""" Reads the config file and returns the value of the variable passed as argument """

import configparser
import os


def get_setting(header, variable):
    """Reads the config file and returns the value of the variable passed as argument"""

    config_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../images.ini"
    )
    if not config_file_path:
        return RuntimeError("images.ini does not exist in the root of the project")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    int_variables = ["bins", "n_ic", "n_x_values", "nc"]
    str_variables = ["color_map", "border_color", "tick_color", "x_label", "y_label"]
    bool_variables = ["print_folder"]
    abs_variables = [
        "colorbar_width",
        "colorbar_right_position",
        "letter_padding",
        "plot_size",
        "title_padding",
    ]

    if variable in int_variables:
        return config.getint(header, variable)
    if variable in str_variables:
        return config.get(header, variable)
    if variable in bool_variables:
        return config.getboolean(header, variable)
    if variable in abs_variables:
        return config.getfloat(header, variable)
    return config.getfloat(header, variable) * config.getfloat("COMMON", "plot_size")
