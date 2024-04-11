#!/usr/bin/env python3

import os
import subprocess

from common_modules.get_config import get_config

EXE = get_config("exe")

source_folder=f"{os.environ['HOME']}/code/{EXE}/results/"
destination_folder=f"{os.environ['STORE']}/code/{EXE}/results/"

rsync_command = [
    "rsync",
    "--archive",
    "--info=progress2",
    "--exclude=*.out",
    "--exclude=*.tmp",
    "--exclude=*.log",
    "--exclude=*.test",
    "--exclude=store",
    "--rsh=ssh",
    source_folder,
    destination_folder
]
subprocess.run(rsync_command, check=True)

