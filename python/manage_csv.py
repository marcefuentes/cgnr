
!/usr/bin/env python3

import os
import tools.csv_tools as tt

def main():
  root_dir = os.getcwd()
  tt.remove_columns_from_csvs(root_dir, ["a2low", "a2high"], "*.frq")
  tt.divide_by_2(root_dir, "w", "*.csv")

if __name__ == "__main__":
  main()

