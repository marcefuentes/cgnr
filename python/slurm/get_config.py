
# Description: This module reads the config file and returns the value of the variable passed as argument

import configparser
import os

def get_config(variable):

    config_file_path = os.environ.get('CONFIG_FILE')
    if not config_file_path:
      return RuntimeError("CONFIG_FILE environment variable not set")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    if variable in config['DEFAULT']:
        if variable == "hours" or variable == "number_of_lines":
            return config.getint('DEFAULT', variable)
        else:
            return config.get('DEFAULT', variable)
    else:
        return RuntimeError(f"{variable} not found in {config_file_path}")
