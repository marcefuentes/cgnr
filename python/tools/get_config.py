
# Description: This module reads the config file and returns the value of the variable passed as argument

import configparser
import os

import tools.colors as cc

def get_config(variable):

    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config.ini")
    if not config_file_path:
      return RuntimeError("config.ini does not exist in the root of the project")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    if config.has_option('DEFAULT', variable):
        if variable in ("hours", "number_of_lines"):
            return config.getint('DEFAULT', variable)
        elif variable in ("alpha_min", "alpha_max", "loges_min", "loges_max"):
            return config.getfloat('DEFAULT', variable)
        elif variable in ("output_file_extensions", "constraints"):
            return config.get("DEFAULT", variable).split(",")
        else:
            return config.get('DEFAULT', variable)
    else:
        print(f"{cc.bold}{cc.red}{variable} not found in {config_file_path}{cc.reset}")
        return 0
