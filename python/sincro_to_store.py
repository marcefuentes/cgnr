#!/usr/bin/env python3

import configparser
import os
import subprocess

config_file_path = os.environ.get('CONFIG_FILE')
if not config_file_path:
  raise RuntimeError("CONFIG_FILE environment variable not set")

config = configparser.ConfigParser()
config.read(config_file_path)
exe = config["DEFAULT"]["exe"]

source_folder=f"$HOME/code/{exe}/results/"
destination=f"$STORE/code/{exe}/results/"

rsync_command = ["rsync",
                 "--archive",
                 "--info=progress2",
                 "--exclude=*.out",
                 "--exclude=*.tmp",
                 "--exclude=*.log",
                 "--exclude=store",
                 "--rsh=ssh",
                 source_folder,
                 destination_folder]
subprocess.run(rsync_command, check=True)

