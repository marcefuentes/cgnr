#!/usr/bin/env python3

import configparser
import os
import subprocess

remote = "cesga"

config_file_path = os.environ.get('CONFIG_FILE')
if not config_file_path:
  raise RuntimeError("CONFIG_FILE environment variable not set")

config = configparser.ConfigParser()
config.read(config_file_path)
exe = config["DEFAULT"]["exe"]

if remote == "cesga":
    source_folder=f"/mnt/netapp2/Store_uni/home/ulc/ba/mfu/code/{exe}/results/"
elif remote == "ci":
    source_folder=f"/home/marcelino/code/{exe}/results/"
else:
    print("Error: remote must be 'cesga' or 'ci'")
    exit()

destination_folder=f"/home/marcelino/code/{exe}/results/"

rsync_command = ["rsync", "--archive", "--info=progress2", "--compress", "--exclude=*.log", "--exclude=*.png", "--rsh=ssh", f"{remote}:{source_folder}", destination_folder]
subprocess.run(rsync_command, check=True)

