#!/usr/bin/env python

import os

import tools.colors as cc
from slurm.get_config import get_config
from slurm.tools import get_qos_limit, get_squeue_stats

queues = get_config("queues")

print()
print(f"{'Queue':<7}{'Max':<5}{'Running':<9}{'Pending':<9}{'Free':<9}")

for queue in queues:

    max_submit = get_qos_limit(queue, "maxsubmit")
    max_running = get_qos_limit(queue, "maxjobspu")
    running_jobs = get_squeue_stats("qos", queue, "running")
    pending_jobs = get_squeue_stats("qos", queue, "pending")
    free_slots = max_submit - running_jobs - pending_jobs

    print(f"{queue:<4}", end = "")
    print(f"{max_running:>6}", end = "")
    print(f"{cc.bold}{cc.yellow if running_jobs < max_running else cc.green}{running_jobs:>9}{cc.reset}", end = "")
    print(f"{cc.bold}{cc.red if pending_jobs == 0 else cc.white}{pending_jobs:>9}{cc.reset}", end = "")
    print(f"{cc.bold}{cc.cyan}{free_slots:>5}{cc.reset}")

print()
