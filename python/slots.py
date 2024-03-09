#! /usr/bin/env python

import mycolors as c
import myslurm
import os

queues = ["clk", "epyc"]

print()
print(f"{'Queue':<6} {'Running':<8} {'Max':<4} {'Pending':<8} {'Free':<8}")
print(f"{'-----':<6} {'-------':<8} {'---':<4} {'-------':<8} {'----':<8}")

for queue in queues:

    max_submit = myslurm.get_max_slots(queue, "maxsubmit")
    max_running = myslurm.get_max_slots(queue, "maxjobspu")
    running_jobs = myslurm.get_slots(queue, "RUNNING")
    pending_jobs = myslurm.get_slots(queue, "PENDING")
    free_slots = max_submit - running_jobs - pending_jobs

    print(f"{queue:<8} {c.bold}{c.yellow if running_jobs < max_running else c.green}{running_jobs:>5}{c.reset_format} {max_running:>4} {c.red if pending_jobs == 0 else c.reset_format}{c.bold}{pending_jobs:>8}{c.reset_format} {c.bold}{c.cyan}{free_slots:>5}{c.reset_format}") 

print()
