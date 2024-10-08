#!/usr/bin/env python3

""" Synchronize results from remote server to local machine """

import os
import subprocess


def main():
    """Main function"""

    remote = "cesga"

    exe = os.environ["PROJECT"]
    folders = ["results", "results_scatter"]

    for folder in folders:
        if remote == "cesga":
            source_folder = f"/mnt/netapp2/Store_uni/home/ulc/ba/mfu/code/{exe}/{folder}/"
        else:
            source_folder = f"/home/marcelino/code/{exe}/{folder}/"

        destination_folder = f"/home/marcelino/code/{exe}/{folder}/"

        rsync_command = [
            "rsync",
            "--archive",
            "--info=progress2",
            "--compress",
            "--exclude=*.sh",
            "--exclude=*.png",
            "--rsh=ssh",
            f"{remote}:{source_folder}",
            destination_folder,
        ]
        subprocess.run(rsync_command, check=True)


if __name__ == "__main__":
    main()
