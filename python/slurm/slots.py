#!/usr/bin/env python

import os

import slurm_tools.slurm_tools as st
import tools.colors as cc
from tools.get_config import get_config

constraints = get_config("constraints")

print()
print(f"{'Queue':<13}{'Max':>5}{'Running':>9}{'Pending':>9}{'Free':>6}")

for constraint in constraints:

    qos_name = st.get_qos_name(constraint)
    max_submit = st.get_qos_limit(constraint, "maxsubmit")
    max_running = st.get_qos_limit(constraint, "maxjobspu")
    running_jobs = st.get_squeue_stats("qos", constraint, "running")
    pending_jobs = st.get_squeue_stats("qos", constraint, "pending")
    free_slots = max_submit - running_jobs - pending_jobs

    print(f"{qos_name:<13}", end = "")
    print(f"{max_running:>5}", end = "")
    print(f"{cc.yellow}{cc.bold if running_jobs == max_running else cc.yellow}{running_jobs:>9}{cc.reset}", end = "")
    print(f"{cc.red if pending_jobs == 0 else cc.white}{pending_jobs:>9}{cc.reset}", end = "")
    print(f"{cc.bold}{cc.cyan}{free_slots:>6}{cc.reset}")

print()
