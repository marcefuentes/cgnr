#!/usr/bin/env python3

from myget_config import get_config
import subprocess

remote = "cesga"

try:
    exe = get_config("exe")
except RuntimeError as e:
    print(e)
    exit()

source_folder=f"$HOME/code/{exe}/results/"
destination_folder=f"$STORE/code/{exe}/results/"

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

