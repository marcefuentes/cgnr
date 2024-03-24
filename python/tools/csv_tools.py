
import csv
import os
import pandas as pd

import tools.csv_tools
from slurm.get_config import get_config

def call_function(function_name, *args, **kwargs):
    # Get the function object using getattr
    function = getattr(tools.csv_tools, function_name)

    if not callable(function):
        raise AttributeError(f"Function '{function_name}' not found in csv_tools.py")

    # Call the function with provided arguments
    return function(*args, **kwargs)

def add_headers():

    extensions = get_config("output_file_extensions")

    for extension in extensions:
        files = [f for f in os.listdir('.') if f.endswith(extension)]
        with open(files[0]) as f:
            headers = f.readline().strip()
        for file in files:
            with open(file, "r+") as f:
                content = f.read()
                if content.startswith(headers):
                    continue
                else:
                    f.seek(0, 0)
                    f.write(headers + "\n" + content)

def remove_extra_headers():

    extensions = get_config("output_file_extensions")

    for extension in extensions:
        for file in os.listdir('.'):
            if file.endswith(extension):
                with open(file, "r") as f:
                    headers = f.readline().strip()
                    content = f.read()
                if content.startswith(headers + "\n"):
                    with open(file, "w") as f:
                        f.write(content)
                    print(f"Removed extra headers from {file}")

def remove_columns_from_csvs(extension, columns_to_remove):
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(full_path)
                    if any(col in df.columns for col in columns_to_remove):
                        df.drop(columns_to_remove, inplace=True)
                        df.to_csv(full_path, index=False)  # Avoid writing index column
                    else:
                        print(f"Info: Skipping {full_path} - Columns not found")
                except FileNotFoundError:
                    print(f"Error: File not found: {full_path}")
                except Exception as e:
                    print(f"Error processing file {full_path}: {e}")

def divide_by_2(extension, column_to_change):
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                df = pd.read_csv(full_path)
                for col in df.columns:
                    if col.startswith(column_to_change):
                        df[col] = (df[col] / 2.0).round(6)
                df.to_csv(file_path, index=False)

def move_time():
    input_extension = ".gl2"
    output_extension = ".glo"

    for c in range(101, 542):
        input_file = f"{c}{input_extension}"
        output_file = f"{c}{output_extension}"
        if os.path.isfile(input_file):
            with open(input_file, "r") as f:
                line = f.readline()
                while line:
                    if line.startswith("TimeElapsed"):
                        time = line
                        break
                    line = f.readline()
            with open(output_file, "r") as f:
                content = f.read()
            with open(output_file, "w") as f:
                f.write(content)
                f.write(time)
            os.remove(input_file)
