
import os
import pandas as pd

def add_headers(extension):
    with open(f"101{extension}") as f:
        headers = f.readline().strip()

    for c in range(102, 542):
        name = f"{c}{extension}"
        if not os.path.isfile(name):
            with open(name, "w") as f:
                f.write(f"{headers}\n")

def remove_columns_from_csvs(root_dir, columns_to_remove, extension):
    for root, _, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(extension):
                full_path = os.path.join(root, filename)
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

def divide_by_2(root_dir, column_to_change, extension):
    for root, _, files in os.walk('.'):
        for filename in files:
            if filename.endswith(extension):
                full_path = os.path.join(root, filename)
                df = pd.read_csv(full_path)
                for col in df.columns:
                    if col.startswith(column_to_change):
                        df[col] = (df[col] / 2.0).round(6)
                df.to_csv(file_path, index=False)

def delete_first_line_if_file_has_11_lines():
    extensions = [".csv", ".frq"]
    for c in range(101, 542):
        number_of_lines_to_keep = 10  # Use a descriptive variable name
        for extension in extensions:
            filename = f"{c}{extension}"
            if not os.path.isfile(filename):
                return  # Skip non-existent files

            with open(filename, "r") as f:
                line_count = sum(1 for line in f)

            if line_count != number_of_lines_to_keep + 1:
                return  # Skip files with incorrect line count

            with open(filename, "r") as f:
                lines = f.readlines()

            with open(filename, "w") as f:
                f.writelines(lines[1:])

def move_time:
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
