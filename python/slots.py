#!/usr/bin/env python

import os

import tools.colors as cc
from tools.get_config import get_config
from slurm.tools import get_qos_limit, get_squeue_stats

constraints = get_config("constraints")

print()
print(f"{'Queue':<7}{'Max':<5}{'Running':<9}{'Pending':<9}{'Free':<9}")

for constraint in constraints:

    max_submit = get_qos_limit(constraint, "maxsubmit")
    max_running = get_qos_limit(constraint, "maxjobspu")
    running_jobs = get_squeue_stats("qos", constraint, "running")
    pending_jobs = get_squeue_stats("qos", constraint, "pending")
    free_slots = max_submit - running_jobs - pending_jobs

    print(f"{constraint:<4}", end = "")
    print(f"{max_running:>6}", end = "")
    print(f"{cc.bold}{cc.yellow if running_jobs < max_running else cc.green}{running_jobs:>9}{cc.reset}", end = "")
    print(f"{cc.bold}{cc.red if pending_jobs == 0 else cc.white}{pending_jobs:>9}{cc.reset}", end = "")
    print(f"{cc.bold}{cc.cyan}{free_slots:>5}{cc.reset}")

print()
