"""Module to perform operations on CSV files."""

import os
import pandas as pd

from common_modules.get_config import get_config


def add_headers():
    """Add headers to files that don't have them."""

    extensions = get_config("output_file_extensions")

    for extension in extensions:
        files = [f for f in os.listdir(".") if f.endswith(extension)]
        with open(files[0], "r", encoding="utf-8") as f:
            headers = f.readline().strip()
        for file in files:
            with open(file, "r+", encoding="utf-8") as f:
                content = f.read()
                if content.startswith(headers):
                    continue
                f.seek(0, 0)
                f.write(headers + "\n" + content)


def call_function(function_name, *args, **kwargs):
    """Function to call a function based on its name (optional)."""

    functions = {
        "add_headers": add_headers,
        # Add more functions here if needed
    }

    if function_name not in functions:
        raise AttributeError(f"Function '{function_name}' not found in csv_tools.py")

    return functions[function_name](*args, **kwargs)


def divide_by_2(extension, column_to_change):
    """Divide values in a column by 2."""

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                df = pd.read_csv(full_path)
                for col in df.columns:
                    if col.startswith(column_to_change):
                        df[col] = (df[col] / 2.0).round(6)
                df.to_csv(full_path, index=False)


def move_time():
    """Move the TimeElapsed line from .gl2 to .glo files."""

    input_extension = ".gl2"
    output_extension = ".glo"

    for c in range(101, 542):
        input_file = f"{c}{input_extension}"
        output_file = f"{c}{output_extension}"
        if os.path.isfile(input_file):
            with open(input_file, "r", encoding="utf-8") as f:
                line = f.readline()
                while line:
                    if line.startswith("TimeElapsed"):
                        time = line
                        break
                    line = f.readline()
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
                f.write(time)
            os.remove(input_file)


def remove_columns_from_csvs(extension, columns_to_remove):
    """Remove columns from CSV files."""

    for root, _, files in os.walk("."):
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


def remove_extra_headers():
    """Remove extra headers from files."""

    extensions = get_config("output_file_extensions")

    for extension in extensions:
        for file in os.listdir("."):
            if file.endswith(extension):
                with open(file, "r", encoding="utf-8") as f:
                    headers = f.readline().strip()
                    content = f.read()
                if content.startswith(headers + "\n"):
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Removed extra headers from {file}")
