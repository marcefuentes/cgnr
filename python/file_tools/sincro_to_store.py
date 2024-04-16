#!/usr/bin/env python3

""" Syncronize the results folder to the store folder """

import os
import subprocess

from common_modules.get_config import get_config


def main():
    """Syncronize the results folder to the store folder"""

    exe = get_config("exe")

    source_folder = f"{os.environ['HOME']}/code/{exe}/results/"
    destination_folder = f"{os.environ['STORE']}/code/{exe}/results/"

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
        destination_folder,
    ]
    subprocess.run(rsync_command, check=True)


if __name__ == "__main__":
    main()
