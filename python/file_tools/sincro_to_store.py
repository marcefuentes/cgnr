#!/usr/bin/env python3

""" Syncronize the results folder to the store folder """

import os
import subprocess


def main():
    """Syncronize the results folder to the store folder"""

    exe = os.environ["PROJECT"]
    folders = ["results", "results_scatter"]

    for folder in folders:
        source_folder = f"{os.environ['HOME']}/code/{exe}/{folder}/"
        destination_folder = f"{os.environ['STORE']}/code/{exe}/{folder}/"

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
