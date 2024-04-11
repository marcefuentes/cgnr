
""" This module contains functions to interact with the SLURM scheduler. """

from math import sqrt
import os
import re
import subprocess
import sys

import common_modules.colors as cc
from common_modules.get_config import get_config

def get_qos_name(constraint):
    """ Returns the name of the QOS that corresponds to the given constraint. """
    HOURS = get_config("hours")
    if constraint == "none":
        command = ["scontrol", "show", "partition", "short", "-o"]
        output = subprocess.check_output(command).decode()
        match = re.search(r"MaxTime=(\d+):", output)
        maxtime_hours = int(match.group(1))
        if HOURS >= maxtime_hours:
            return "medium"
        return "short"
    qos_name = f"{constraint}_short"
    command = [
        "sacctmgr",
        "--noheader",
        "--parsable2",
        "show",
        "qos", qos_name,
        "format=maxwall"
    ]
    output = subprocess.check_output(command).decode().strip()
    if output is None:
        print(f"{color.RED}QOS {qos_name} not found{color.RESET}")
        sys.exit()
    maxwall_hours = int(output.split(":", maxsplit=1)[0])
    if HOURS >= maxwall_hours:
        qos_name = f"{constraint}_medium"
    return qos_name

def get_qos_limit(constraint, specification):
    """ Returns the value of the given specification for the given constraint. """
    qos_name = get_qos_name(constraint)
    command = [
        "sacctmgr",
        "--noheader",
        "--parsable2",
        "show",
        "qos", qos_name,
        f"format={specification}"
    ]
    output = subprocess.check_output(command).decode().strip()
    limit = int(output)
    return limit

def slots():
    """ Prints the number of free slots for each QOS. """
    CONSTRAINTS = get_config("constraints")
    total_free_slots = 0
    #print(f"{'Qos':<12}{'Max':>5}{'Running':>9}{'Pending':>5}{'Free':>5}")

    for constraint in CONSTRAINTS:

        qos_name = get_qos_name(constraint)
        max_submit = get_qos_limit(constraint, "maxsubmit")
        max_running = get_qos_limit(constraint, "maxjobspu")
        running = get_squeue_stats("qos", constraint, "running")
        pending = get_squeue_stats("qos", constraint, "pending")
        free_slots = max_submit - running - pending
        total_free_slots += free_slots

        print(f"{qos_name:<12}", end = "")
        if max_running > running:
            print(f"({max_running:>3})", end = "")
        else:
            print(f"{' ' * 5:>5}", end="")
        print(f"{color.YELLOW}{running if running else ' ' * 5:>5}{color.RESET}", end = "")
        print(f"{color.WHITE}{pending if pending else ' ' * 4:>4}{color.RESET}", end = "")
        print(f"{color.BOLD}{color.CYAN}{free_slots if free_slots else '':>4}{color.RESET}")

    return total_free_slots

def get_free_slots(constraint):
    """ Returns the number of free slots for the given constraint. """
    max_submit = get_qos_limit(constraint, "maxsubmit")
    submitted_jobs = get_squeue_stats("qos", constraint, "running,pending")
    free_slots = max_submit - submitted_jobs
    return free_slots

def get_squeue_stats(key, value, state):
    """ Returns the number of jobs that match the given key, value, and state. """
    if key == "qos":
        value = get_qos_name(value)
    key = f"--{key}"
    # %f is the feature (such as the constraint set with sbatch)
    command = [
        "squeue",
        "--states", state,
        "--array",
        "--noheader",
        "--format", "%f",
        key, value
    ]
    output = subprocess.check_output(command).decode().strip().splitlines()
    stats = len(output)
    return stats

def submit_job(current_path_folders, job_array_string, constraint):
    """ Submits a job to the SLURM scheduler. """

    EXE = get_config("exe")
    HOURS = get_config("hours")
    MEMORY = get_config("memory")
    MAIL_USER = get_config("mail_user")

    constraint = "" if constraint == "none" else constraint
    executable = f"/home/ulc/ba/mfu/code/{EXE}/bin/{EXE}"
    variant = current_path_folders[-3]
    mechanism = current_path_folders[-2]
    given = current_path_folders[-1]
    job_name = f"{mechanism}_{given}_{variant}"
    job_time = f"{HOURS}:59:00"
    command = [
        "sbatch",
        "--job-name", job_name,
        "--output", "%a_slurm.out", # %a is the array index
        "--constraint", constraint,
        "--nodes", "1",
        "--tasks", "1",
        "--time", job_time,
        "--mem", MEMORY,
        "--mail-type", "fail",
        "--mail-user", MAIL_USER,
        "--array", job_array_string,
        "--wrap", f"srun {executable} ${{SLURM_ARRAY_TASK_ID}}"
    ]
    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        text=True,
        stderr=subprocess.PIPE
    ) as process:
        stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr

def job_is_queued(current_path_folders, job_array_index):
    """ Returns True if the job with the given job array index is queued. """
    # %j is the job name, %K is the job array index
    command = [
        "squeue",
        "--states", "running,pending",
        "--array",
        "--noheader",
        "--format", "%j,%K"
    ]
    output = subprocess.check_output(command, text="True").strip().splitlines()
    variant = current_path_folders[-3]
    mechanism = current_path_folders[-2]
    given = current_path_folders[-1]
    for line in output:
        if line == f"{mechanism}_{given}_{variant},{job_array_index}":
            return True
    return False

def get_jobs_to_submit(current_path_folders):
    """ Returns a list of job array indices that need to be submitted. """

    INPUT_FILE_EXTENSION = get_config("input_file_extension")
    OUTPUT_FILE_EXTENSION, *_ = get_config("output_file_extensions")
    NUMBER_OF_LINES = get_config("number_of_lines")

    jobs_to_submit = []
    names = [name[:-4] for name in os.listdir() if name.endswith(INPUT_FILE_EXTENSION)]
    start_num = int(names[0])
    end_num = int(names[-1])
    row_length = int(sqrt(float(len(names))))
    current_num = end_num - row_length + 1
    while current_num >= start_num:
        for num in range(current_num, current_num + row_length):
            name = str(num)
            output_file = f"{name}{OUTPUT_FILE_EXTENSION}"
            if os.path.isfile(output_file):
                with open(output_file, "r", encoding="utf-8") as f:
                    current_number_of_lines = sum(1 for line in f)
                if current_number_of_lines < NUMBER_OF_LINES - 1:
                    if job_is_queued(current_path_folders, name):
                        print(f"{color.YELLOW}{name}{color.RESET}", end = " ")
                    else:
                        print(f"{color.RED}{name}{color.RESET}", end = " ")
                        jobs_to_submit.append(name)
                elif current_number_of_lines == NUMBER_OF_LINES - 1:
                    print(f"{color.BOLD}{color.PURPLE}{name}{color.RESET}", end = " ")
                elif current_number_of_lines == NUMBER_OF_LINES:
                    print(f"{color.GREEN}{name}{color.RESET}", end = " ")
                else:
                    print(f"{color.BLUE}{name}{color.RESET}", end = " ")
            else:
                if job_is_queued(current_path_folders, name):
                    print(f"{name}{color.RESET}", end = " ")
                else:
                    print(f"{color.GREY}{name}{color.RESET}", end = " ")
                    jobs_to_submit.append(name)
        print()
        current_num -= row_length

    return jobs_to_submit

def remove_files(jobs_to_submit):
    """ Removes the output files for the given job array indices. """
    EXTENSIONS = get_config("output_file_extensions")
    for name in jobs_to_submit:
        for extension in EXTENSIONS:
            if os.path.isfile(f"{name}{extension}"):
                os.remove(f"{name}{extension}")
            else:
                continue
