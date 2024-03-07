from glob import glob
import os
import time

# The object of this script is to delete the columns in columns in each csv file in all directories and subdirectories of the current directory. 

start_time = time.perf_counter()

# Options

columns_to_remove = ["a2low", "a2high"]
extension = "*.frq"

# Get the names of the subdirectories in the current directory
subdirectories = glob("*/")

# Loop through the subdirectories
for subdirectory in subdirectories:
    # cd into the subdirectory
    os.chdir(subdirectory)
    # Get the names of the subdirectories in this subdirectory
    mechanisms = glob("*/")
    # Loop through the subdirectories
    for mechanism in mechanisms:
        os.chdir(mechanism)
        # Get the names of the subdirectories in this subdirectory
        givens = glob("*/")
        # Loop through the subdirectories
        for given in givens:
            os.chdir(given)
            # Get the names of the csv files in this subdirectory
            csv_files = glob(extension)
            # Loop through the csv files
            for csv_file in csv_files:
                # Read the csv file into a list of lines
                with open(csv_file, 'r') as file:
                    lines = file.readlines()

                # Identify the column indices to remove
                header = lines[0].strip().split(',')
                indices_to_remove = [header.index(column) for column in columns_to_remove if column in header]

                # Modify each line to remove unwanted columns
                modified_lines = []
                for line in lines:
                    line_values = line.strip().split(',')
                    modified_line = [line_values[i] for i in range(len(line_values)) if i not in indices_to_remove]
                    modified_lines.append(','.join(modified_line))

                # Write the modified lines back to the file
                with open(csv_file, 'w') as file:
                    file.write('\n'.join(modified_lines))

            # cd out of the subdirectory
            print(f"{subdirectory}{mechanism}{given}")
            os.chdir("../")
        # cd out of the subdirectory
        os.chdir("../")
    # cd out of the subdirectory
    os.chdir("../")

end_time = time.perf_counter()
print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")

