#!/usr/bin/env python

import os

import submit
import modules.slurm_tools as st
import tools.colors as cc
from tools.get_config import get_config

def main():

    constraints = get_config("constraints")
    total_free_slots = 0

    print()
    #print(f"{'Qos':<12}{'Max':>5}{'Running':>9}{'Pending':>5}{'Free':>5}")

    for constraint in constraints:

        qos_name = st.get_qos_name(constraint)
        max_submit = st.get_qos_limit(constraint, "maxsubmit")
        max_running = st.get_qos_limit(constraint, "maxjobspu")
        running = st.get_squeue_stats("qos", constraint, "running")
        pending = st.get_squeue_stats("qos", constraint, "pending")
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

if __name__ == "__main__":
    main()
