""" Submit jobs """

import logging
import os
import sys

from common_modules.colors import COLORS as colors
from modules.slurm_tools import submit_job


def process_jobs(current_path_folders, job_array_string, constraint, test):
    """Submit jobs"""

    exe = os.environ["PROJECT"]
    if test:
        log_file_extension = ".test"
    else:
        log_file_extension = ".log"
    log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit{log_file_extension}"
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    current_path_print = "/".join(current_path_folders[-3:])
    info = f"{current_path_print}/{job_array_string} to {constraint}"
    if test:
        print(f"Would submit {info}")
        return_code = 0
        stderr = "Test"
        stdout = "Test"
    else:
        return_code, stdout, stderr = submit_job(
            current_path_folders, job_array_string, constraint
        )
    if return_code != 0:
        print(
            f"{colors['red']}sbatch command failed with return code {return_code}{colors['reset']}"
        )
        if stderr:
            print(stderr)
            logging.error(stderr)
        sys.exit()
    else:
        for line in stdout.split("\n"):
            if line:
                print(line)
                logging.info(line)
    logging.info(info)
    print(f"{colors['green']}{info}{colors['reset']}")
