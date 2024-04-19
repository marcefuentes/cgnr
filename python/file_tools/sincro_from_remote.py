#!/usr/bin/env python3

""" Synchronize results from remote server to local machine """

import subprocess

from common_modules.get_config import get_config


def main():
    """Main function"""

    remote = "cesga"

    exe = get_config("exe")

    if remote == "cesga":
        source_folder = f"/mnt/netapp2/Store_uni/home/ulc/ba/mfu/code/{exe}/results/"
    elif remote == "ci":
        source_folder = f"/home/marcelino/code/{exe}/results/"

    destination_folder = f"/home/marcelino/code/{exe}/results/"

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
