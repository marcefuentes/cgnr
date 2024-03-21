#!/usr/bin/env python3

import os
import subprocess
from slurm.get_config import get_config

try:
    exe = get_config("exe")
except RuntimeError as e:
    print(e)
    exit()

source_folder=f"{os.environ['HOME']}/code/{exe}/results/"
destination_folder=f"{os.environ['STORE']}/code/{exe}/results/"

rsync_command = ["rsync",
                 "--archive",
                 "--info=progress2",
                 "--exclude=*.out",
                 "--exclude=*.tmp",
                 "--exclude=*.log",
                 "--exclude=*.test",
                 "--exclude=store",
                 "--rsh=ssh",
                 source_folder,
                 destination_folder]
subprocess.run(rsync_command, check=True)

