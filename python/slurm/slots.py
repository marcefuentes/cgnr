#!/usr/bin/env python

import os

import submit
import slurm_tools.slurm_tools as st
import tools.colors as cc
from tools.get_config import get_config

constraints = get_config("constraints")

print()
#print(f"{'Qos':<12}{'Max':>5}{'Running':>9}{'Pending':>4}{'Free':>4}")

for constraint in constraints:

    qos_name = st.get_qos_name(constraint)
    max_submit = st.get_qos_limit(constraint, "maxsubmit")
    max_running = st.get_qos_limit(constraint, "maxjobspu")
    running_jobs = st.get_squeue_stats("qos", constraint, "running")
    pending_jobs = st.get_squeue_stats("qos", constraint, "pending")
    free_slots = max_submit - running_jobs - pending_jobs

    print(f"{qos_name:<12}", end = "")
    print(f"{max_running:>5}", end = "")
    print(f"{cc.yellow}{cc.bold if running_jobs == max_running else cc.yellow}{running_jobs:>9}{cc.reset}", end = "")
    print(f"{cc.red if pending_jobs == 0 else cc.white}{pending_jobs:>4}{cc.reset}", end = "")
    print(f"{cc.bold}{cc.cyan}{free_slots:>4}{cc.reset}")

    if free_slots:
        print(f"\n{cc.bold}Submit {cc.cyan}{free_slots}{cc.reset} jobs {cc.yesno} ", end="")
        user_input = input()
        if user_input.lower() == "n":
            exit()
        submit.main()
print()
