
from math import sqrt
import os
import re
import subprocess
import tools.colors as cc
from slurm.get_config import get_config

def get_qos_name(queue):
    try:
        hours = get_config("hours")
    except RuntimeError as e:
        print(f"{cc.bold}{cc.red}{e}{cc.reset_format}")
        exit()
    qos_name = f"{queue}_short"
    command = ["sacctmgr", "--noheader", "--parsable2", "show", "qos", qos_name, "format=maxwall"]
    output = subprocess.check_output(command)
    if output is None:
        print(f"{red}QOS {qos_name} not found{reset_format}")
        exit()
    maxwall = output.decode().strip()
    maxwall_hours = int(maxwall.split(":")[0])
    if hours >= maxwall_hours:
        qos_name = f"{queue}_medium"
    return qos_name

def get_qos_limit(queue, specification):
    qos_name = get_qos_name(queue)
    command = ["sacctmgr", "--noheader", "--parsable2", "show", "qos", qos_name, f"format={specification}"]
    output = subprocess.check_output(command)
    limit = output.decode().strip()
    limit = int(output)
    return limit

def get_free_slots(queue):
    max_submit = get_qos_limit(queue, "maxsubmit")
    submitted_jobs = get_squeue_stats("qos", queue, "running,pending")
    free_slots = max_submit - submitted_jobs
    return free_slots

def get_squeue_stats(key, value, state):
    if key == "qos":
        value = get_qos_name(value)
    # %f is the feature (such as the constraint set with sbatch)
    command = f"squeue --states={state} --array --noheader --format=%f --{key}={value} | wc --lines"
    output = subprocess.check_output(command, shell=True)
    stats = output.decode().strip()
    stats = int(stats)
    return stats

def submit_job(current_path_folders, job_array_string, queue):

    try: 
        exe = get_config("exe")
    except RuntimeError as e:
        return -1, None, e
    try:
        hours = get_config("hours")
    except RuntimeError as e:
        return -1, None, e
    try:
        memory = get_config("memory")
    except RuntimeError as e:
        return -1, None, e
    try:
        mail_user = get_config("mail_user")
    except RuntimeError as e:
        return -1, None, e

    executable = f"/home/ulc/ba/mfu/code/{exe}/bin/{exe}"
    variant = current_path_folders[-3]
    mechanism = current_path_folders[-2]
    given = current_path_folders[-1]
    job_name = f"{mechanism}_{given}_{variant}"
    job_time = f"{hours}:59:00"
    command = ["sbatch",
               "--job-name", job_name,
               "--output=%a_slurm.out", # %a is the array index
               "--constraint", queue,
               "--nodes=1",
               "--tasks=1",
               "--time", job_time,
               "--mem", memory,
               "--mail-type=fail",
               "--mail-user", mail_user,
               "--array", job_array_string,
               "--wrap", f"srun {executable} ${{SLURM_ARRAY_TASK_ID}}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr

def job_is_queued(current_path_folders, job_array_index):
    # %j is the job name, %K is the job array index
    command = ["squeue", "--states", "running,pending", "--array", "--noheader", "--format=%j,%K"]
    output = subprocess.check_output(command, text=True).strip().split("\n")
    variant = current_path_folders[-3]
    mechanism = current_path_folders[-2]
    given = current_path_folders[-1]
    for line in output:
        if line == f"{mechanism}_{given}_{variant},{job_array_index}":
            return True
    return False

def get_jobs_to_submit(current_path_folders):

    try:
        input_file_extension = get_config("input_file_extension")
    except RuntimeError as e:
        print(f"{cc.red}{e}{cc.reset_format}")
        exit()
    try:
        output_file_extension = get_config("first_output_file_extension")
    except RuntimeError as e:
        print(f"{cc.red}{e}{cc.reset_format}")
        exit()
    try:
        number_of_lines = get_config("number_of_lines")
    except RuntimeError as e:
        return -1, None, e

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
                        print(f"{cc.bold}{cc.yellow}{name}{cc.reset_format}", end = " ")
                    else:
                        print(f"{cc.bold}{cc.red}{name}{cc.reset_format}", end = " ")
                        jobs_to_submit.append(name)
                elif current_number_of_lines == number_of_lines - 1:
                    print(f"{cc.bold}{cc.purple}{name}{cc.reset_format}", end = " ")
                elif current_number_of_lines == number_of_lines:
                    print(f"{cc.bold}{cc.green}{name}{cc.reset_format}", end = " ")
                else:
                    print(f"{cc.bold}{cc.blue}{name}{cc.reset_format}", end = " ")
            else:
                if job_is_queued(current_path_folders, name):
                    print(f"{cc.bold}{name}{cc.reset_format}", end = " ")
                else:
                    print(f"{cc.bold}{cc.grey}{name}{cc.reset_format}", end = " ")
                    jobs_to_submit.append(name)
        print()
        current_num -= row_length

    return jobs_to_submit

def remove_files(jobs_to_submit):
    try:
        first_output_file_extension = get_config("first_output_file_extension")
    except RuntimeError as e:
        print(f"{cc.red}{e}{cc.reset_format}")
        exit()
    try:
        second_output_file_extension = get_config("second_output_file_extension")
    except RuntimeError as e:
        print(f"{cc.red}{e}{cc.reset_format}")
        exit()

    output_file_extensions = [first_output_file_extension, second_output_file_extension]
    for name in jobs_to_submit:
        for extension in output_file_extensions:
            if os.path.isfile(f"{name}{extension}"):
                os.remove(f"{name}{extension}")
            else:
                continue

