""" Reads the config file and returns the value of the variable passed as argument """

import configparser
import os


def get_setting(header, variable):
    """Reads the config file and returns the value of the variable passed as argument"""

    project_python = os.environ.get("PROJECT_PYTHON")
    config_file_path = os.path.join(project_python, "images", "images.ini")
    if not config_file_path:
        return RuntimeError("images.ini does not exist in the root of the project")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    abs_variables = [
        "colorbar_width",
        "colorbar_right_position",
        "letter_padding",
        "plot_size",
        "title_padding",
    ]
    bool_variables = ["print_folder"]
    int_variables = ["n_ic", "n_x_values", "nc", "nr"]
    list_variables = ["all_traits"]
    str_variables = [
        "color_map",
        "border_color",
        "given_folder",
        "marker",
        "tick_color",
        "x_label",
        "y_label",
    ]

    if variable in abs_variables:
        value = config.getfloat(header, variable)
    elif variable in bool_variables:
        value = config.getboolean(header, variable)
    elif variable in int_variables:
        value = config.getint(header, variable)
    elif variable in list_variables:
        value = config.get(header, variable).split(",")
    elif variable in str_variables:
        value = config.get(header, variable)
    else:
        value = config.getfloat(header, variable) * config.getfloat("COMMON", "plot_size")

    return value


def get_titles(keys):
    """Reads the config file and returns the value of the variable passed as argument"""

    project_python = os.environ.get("PROJECT_PYTHON")
    config_file_path = os.path.join(project_python, "images", "titles.ini")
    if not config_file_path:
        return RuntimeError("titles.ini does not exist in the root of the project")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    titles = []
    for key in keys:
        if not key:
            titles.append("")
            continue
        title = config.get("DEFAULT", key).replace("\\n", "\n")
        titles.append(title)

    return titles
