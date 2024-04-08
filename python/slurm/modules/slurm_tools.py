
from math import sqrt
import os
import re
import subprocess

import tools.colors as cc
from tools.get_config import get_config

def get_qos_name(constraint):
    hours = get_config("hours")
    if constraint == "none":
        command = ["scontrol", "show", "partition", "short", "-o"]
        output = subprocess.check_output(command).decode()
        match = re.search(r"MaxTime=(\d+):", output)
        maxtime_hours = int(match.group(1))
        if hours >= maxtime_hours:
            return "medium"
        else:
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
        print(f"{red}QOS {qos_name} not found{reset}")
        exit()
    maxwall_hours = int(output.split(":")[0])
    if hours >= maxwall_hours:
        qos_name = f"{constraint}_medium"
    return qos_name

def get_qos_limit(constraint, specification):
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

    constraints = get_config("constraints")
    total_free_slots = 0

    print()
    #print(f"{'Qos':<12}{'Max':>5}{'Running':>9}{'Pending':>5}{'Free':>5}")

    for constraint in constraints:

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
        print(f"{cc.yellow}{running if running else ' ' * 5:>5}{cc.reset}", end = "")
        print(f"{cc.white}{pending if pending else ' ' * 4:>4}{cc.reset}", end = "")
        print(f"{cc.bold}{cc.cyan}{free_slots if free_slots else '':>4}{cc.reset}")

    if total_free_slots:
        exe = get_config("exe")
        last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
        if os.path.isfile(last_job_file):
            print(f"\n{cc.bold}Submit {cc.cyan}{total_free_slots}{cc.reset}{cc.bold} jobs{cc.reset} {cc.yesno} ", end="")
            user_input = input()
            if user_input.lower() == "n":
                print()
                exit()
            submit.main()
        else:
            print(f"\nTo submit jobs, go to a variant folder with no running or finished jobs and run submit\n")
    else:
        print()

def get_free_slots(constraint):
    max_submit = get_qos_limit(constraint, "maxsubmit")
    submitted_jobs = get_squeue_stats("qos", constraint, "running,pending")
    free_slots = max_submit - submitted_jobs
    return free_slots

def get_squeue_stats(key, value, state):
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

    exe = get_config("exe")
    hours = get_config("hours")
    memory = get_config("memory")
    mail_user = get_config("mail_user")

    constraint = "" if constraint == "none" else constraint
    executable = f"/home/ulc/ba/mfu/code/{exe}/bin/{exe}"
    variant = current_path_folders[-3]
    mechanism = current_path_folders[-2]
    given = current_path_folders[-1]
    job_name = f"{mechanism}_{given}_{variant}"
    job_time = f"{hours}:59:00"
    command = [
        "sbatch",
        "--job-name", job_name,
        "--output", "%a_slurm.out", # %a is the array index
        "--constraint", constraint,
        "--nodes", "1",
        "--tasks", "1",
        "--time", job_time,
        "--mem", memory,
        "--mail-type", "fail",
        "--mail-user", mail_user,
        "--array", job_array_string,
        "--wrap", f"srun {executable} ${{SLURM_ARRAY_TASK_ID}}"
    ]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        text=True,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr

def job_is_queued(current_path_folders, job_array_index):
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

    input_file_extension = get_config("input_file_extension")
    output_file_extension, *_ = get_config("output_file_extensions")
    number_of_lines = get_config("number_of_lines")

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
                with open(output_file) as f:
                    current_number_of_lines = sum(1 for line in f)
                if current_number_of_lines < number_of_lines - 1:
                    if job_is_queued(current_path_folders, name):
                        print(f"{cc.yellow}{name}{cc.reset}", end = " ")
                    else:
                        print(f"{cc.red}{name}{cc.reset}", end = " ")
                        jobs_to_submit.append(name)
                elif current_number_of_lines == number_of_lines - 1:
                    print(f"{cc.bold}{cc.purple}{name}{cc.reset}", end = " ")
                elif current_number_of_lines == number_of_lines:
                    print(f"{cc.green}{name}{cc.reset}", end = " ")
                else:
                    print(f"{cc.blue}{name}{cc.reset}", end = " ")
            else:
                if job_is_queued(current_path_folders, name):
                    print(f"{name}{cc.reset}", end = " ")
                else:
                    print(f"{cc.grey}{name}{cc.reset}", end = " ")
                    jobs_to_submit.append(name)
        print()
        current_num -= row_length

    return jobs_to_submit

def remove_files(jobs_to_submit):
    extensions = get_config("output_file_extensions")
    for name in jobs_to_submit:
        for extension in extensions:
            if os.path.isfile(f"{name}{extension}"):
                os.remove(f"{name}{extension}")
            else:
                continue

