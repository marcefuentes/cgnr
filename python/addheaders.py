#! /usr/bin/env python

import os

extension = ".frq"

with open(f"101{extension}") as f:
    headers = f.readline().strip()

for c in range(102, 542):
    name = f"{c}{extension}"
    if not os.path.isfile(name):
        with open(name, "w") as f:
            f.write(f"{headers}\n")
