#! /usr/bin/env python

from glob import glob
import os
import time

import pandas as pd

start_time = time.perf_counter()
this_file = os.path.basename(__file__)
file_name = this_file.split(".")[0]

columns = ["alpha",
           "logES",
           "Given",
           "Time",
           "wmean",
           "a2Seenmean",
           "ChooseGrainmean",
           "MimicGrainmean",
           "ImimicGrainmean"]

subdirectories = glob("*/")

for subdirectory in subdirectories:
    os.chdir(subdirectory)
    mechanisms = glob("*/")
    for mechanism in mechanisms:
        os.chdir(mechanism)
        givens = glob("*/")
        for given in givens:
            df = pd.concat([pd.read_csv(f) for f in glob(f"{given}*.csv")])
            df = df[columns]
            df.to_csv(f"{given[:-1]}.csv", index=False)
            os.system(f"rm -rf {given}")
        os.chdir("../")
    os.chdir("../")

end_time = time.perf_counter()
print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")
