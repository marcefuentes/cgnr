
import os
import pandas as pd

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

def main():
  root_dir = os.getcwd()
  remove_columns_from_csvs(root_dir, ["a2low", "a2high"], "*.frq")
  divide_by_2(root_dir, "w", "*.csv")

if __name__ == "__main__":
  main()

