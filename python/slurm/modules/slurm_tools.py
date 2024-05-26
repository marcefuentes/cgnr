""" This module contains functions to interact with the SLURM scheduler. """

from math import sqrt
import os
import re
import subprocess
import sys

from common_modules.colors import COLORS as colors
from common_modules.settings import SETTINGS as settings


def get_free_slots(constraint):
    """Returns the number of free slots for the given constraint."""

    max_submit = get_qos_limit(constraint, "maxsubmit")
    submitted_jobs = get_squeue_stats("qos", constraint, "running,pending")
    free_slots = max_submit - submitted_jobs
    return free_slots


def get_jobs_to_submit(current_path_folders):
    """Returns a list of job array indices that need to be submitted."""

    input_file_extension = settings["input_file_extension"]
    output_file_extension, *_ = settings["output_file_extensions"]
    number_of_lines = settings["number_of_lines"]

    jobs_to_submit = []
    names = [name[:-4] for name in os.listdir() if name.endswith(input_file_extension)]
    start_num = int(names[0])
    end_num = int(names[-1])
    row_length = int(sqrt(float(len(names))))
    current_num = end_num - row_length + 1
    while current_num >= start_num:
        for num in range(current_num, current_num + row_length):
            name = str(num)
            output_file = f"{name}{output_file_extension}"
            if os.path.isfile(output_file):
                with open(output_file, "r", encoding="utf-8") as f:
                    current_number_of_lines = sum(1 for line in f)
                if current_number_of_lines < number_of_lines - 1:
                    if job_is_queued(current_path_folders, name):
                        print(f"{colors['yellow']}{name}{colors['reset']}", end=" ")
                    else:
                        print(f"{colors['red']}{name}{colors['reset']}", end=" ")
                        jobs_to_submit.append(name)
                elif current_number_of_lines == number_of_lines - 1:
                    print(
                        f"{colors['bold']}{colors['purple']}{name}{colors['reset']}",
                        end=" ",
                    )
                elif current_number_of_lines == number_of_lines:
                    print(f"{colors['green']}{name}{colors['reset']}", end=" ")
                else:
                    print(f"{colors['blue']}{name}{colors['reset']}", end=" ")
            else:
                if job_is_queued(current_path_folders, name):
                    print(f"{name}{colors['reset']}", end=" ")
                else:
                    print(f"{colors['grey']}{name}{colors['reset']}", end=" ")
                    jobs_to_submit.append(name)
        print()
        current_num -= row_length

    return jobs_to_submit


def get_squeue_stats(key, value, state):
    """Returns the number of jobs that match the given key, value, and state."""

    if key == "qos":
        value = get_qos_name(value)
    key = f"--{key}"
    # %f is the feature (such as the constraint set with sbatch)
    command = [
        "squeue",
        "--states",
        state,
        "--array",
        "--noheader",
        "--format",
        "%f",
        key,
        value,
    ]
    output = subprocess.check_output(command).decode().strip().splitlines()
    stats = len(output)
    return stats


def get_qos_limit(constraint, specification):
    """Returns the value of the given specification for the given constraint."""

    qos_name = get_qos_name(constraint)
    command = [
        "sacctmgr",
        "--noheader",
        "--parsable2",
        "show",
        "qos",
        qos_name,
        f"format={specification}",
    ]
    output = subprocess.check_output(command).decode().strip()
    limit = int(output)
    return limit


def get_qos_name(constraint):
    """Returns the name of the QOS that corresponds to the given constraint."""

    hours = settings["hours"]
    if constraint == "none":
        command = ["scontrol", "show", "partition", "short", "-o"]
        output = subprocess.check_output(command).decode()
        match = re.search(r"MaxTime=(\d+):", output)
        maxtime_hours = int(match.group(1))
        if hours >= maxtime_hours:
            return "medium"
        return "short"
    qos_name = f"{constraint}_short"
    command = [
        "sacctmgr",
        "--noheader",
        "--parsable2",
        "show",
        "qos",
        qos_name,
        "format=maxwall",
    ]
    output = subprocess.check_output(command).decode().strip()
    if output is None:
        print(f"{colors['red']}QOS {qos_name} not found{colors['reset']}")
        sys.exit()
    maxwall_hours = int(output.split(":", maxsplit=1)[0])
    if hours >= maxwall_hours:
        qos_name = f"{constraint}_medium"
    return qos_name


def job_is_queued(current_path_folders, job_array_index):
    """Returns True if the job with the given job array index is queued."""
    # %j is the job name, %K is the job array index

    command = [
        "squeue",
        "--states",
        "running,pending",
        "--array",
        "--noheader",
        "--format",
        "%j,%K",
    ]
    output = subprocess.check_output(command, text="True").strip().splitlines()
    variant = current_path_folders[-3]
    mechanism = current_path_folders[-2]
    given = current_path_folders[-1]
    for line in output:
        if line == f"{mechanism}_{given}_{variant},{job_array_index}":
            return True
    return False


def remove_files(jobs_to_submit):
    """Removes the output files for the given job array indices."""

    extensions = settings["output_file_extensions"]
    for name in jobs_to_submit:
        for extension in extensions:
            if os.path.isfile(f"{name}{extension}"):
                os.remove(f"{name}{extension}")
            else:
                continue


def slots():
    """Prints the number of free slots for each QOS."""

    constraints = settings["constraints"]
    total_free_slots = 0
    # print(f"{'Qos':<12}{'Max':>5}{'Running':>9}{'Pending':>5}{'Free':>5}")

    for constraint in constraints:

        qos_name = get_qos_name(constraint)
        max_submit = get_qos_limit(constraint, "maxsubmit")
        max_running = get_qos_limit(constraint, "maxjobspu")
        running = get_squeue_stats("qos", constraint, "running")
        pending = get_squeue_stats("qos", constraint, "pending")
        free_slots = max_submit - running - pending
        total_free_slots += free_slots

        print(f"{qos_name: <12}", end="")
        if max_running > running:
            print(f"({max_running:>3})", end="")
        else:
            print(f"{' ' * 5:>5}", end="")
        print(
            f"{colors['yellow']}{running if running else ' ' * 5:>5}{colors['reset']}",
            end="",
        )
        print(
            f"{colors['white']}{pending if pending else ' ' * 4:>4}{colors['reset']}",
            end="",
        )
        print(
            f"{colors['bold']}{colors['cyan']}{free_slots if free_slots else '':>4}{colors['reset']}"
        )

    return total_free_slots


def submit_job(current_path_folders, job_array_string, constraint):
    """Submits a job to the SLURM scheduler."""

    exe = os.environ["PROJECT"]
    hours = settings["hours"]
    memory = settings["memory"]
    mail_user = settings["mail_user"]

    constraint = "" if constraint == "none" else constraint
    executable = f"/home/ulc/ba/mfu/code/{exe}/bin/{exe}"
    job_name = f"{current_path_folders[-2]}"
    job_name += f"_{current_path_folders[-1]}"
    job_name += f"_{current_path_folders[-3]}"
    job_time = f"{hours}:59:00"
    command = [
        "sbatch",
        "--job-name",
        job_name,
        "--output",
        "%a_slurm.out",  # %a is the array index
        "--constraint",
        constraint,
        "--nodes",
        "1",
        "--tasks",
        "1",
        "--time",
        job_time,
        "--mem",
        memory,
        "--mail-type",
        "fail",
        "--mail-user",
        mail_user,
        "--array",
        job_array_string,
        "--wrap",
        f"srun {executable} ${{SLURM_ARRAY_TASK_ID}}",
    ]
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE
    ) as process:
        stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr
