#!/usr/bin/env python

import tools.colors as cc
from slurm.tools import get_qos_limit, get_squeue_stats
import os

queues = ["clk", "epyc"]

print()
print(f"{'Queue':<7}{'Max':<5}{'Running':<9}{'Pending':<9}{'Free':<9}")

for queue in queues:

    max_submit = get_qos_limit(queue, "maxsubmit")
    max_running = get_qos_limit(queue, "maxjobspu")
    running_jobs = get_squeue_stats(queue, "running")
    pending_jobs = get_squeue_stats(queue, "pending")
    free_slots = max_submit - running_jobs - pending_jobs

    print(f"{queue:<4}", end = "")
    print(f"{max_running:>6}", end = "")
    print(f"{cc.bold}{cc.yellow if running_jobs < max_running else cc.green}{running_jobs:>9}{cc.reset_format}", end = "")
    print(f"{cc.bold}{cc.red if pending_jobs == 0 else cc.white}{pending_jobs:>9}{cc.reset_format}", end = "")
    print(f"{cc.bold}{cc.cyan}{free_slots:>5}{cc.reset_format}")

    #{max_running:>6}{cc.bold}{cc.yellow if running_jobs < max_running else cc.green}{running_jobs:>9}{cc.bold}{cc.red if pending_jobs == 0 else cc.white}{pending_jobs:>9}{cc.reset_format} {cc.bold}{cc.cyan}{free_slots:>5}{cc.reset_format}") 

print()
