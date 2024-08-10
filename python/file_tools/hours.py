"""Calculate the total number of hours from all *.glo files in all directories."""

import os


def get_hours_from_file(filepath):
    """
    Extracts the number of hours from the last line of a *.glo file.

    Args:
        filepath: Path to the *.glo file.

    Returns:
        The number of hours extracted from the last line, or 0 if parsing fails.
    """

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            last_line = f.readlines()[
                -1
            ].strip()  # Read last line and remove whitespace
            if last_line.startswith("TimeElapsed,"):
                # Extract time string after comma
                time_str = last_line.split(",")[1]
                if "-" in time_str:  # Extract days (ignored) and hours
                    return int(time_str.split("-")[1].split(":")[0])
                return int(time_str.split(":")[0])  # Extract hours only
            return 0  # Line doesn't start with "TimeElapsed,"
    except FileNotFoundError:
        # Handle potential file not found error
        return 0


def main():
    """Main function."""

    # Replace 'path/to/your/directory' with the actual directory path
    total_hours = sum_hours_from_glo_files("/home/marcelino/code/cgnr/results/")
    print(f"Total hours from all *.glo files: {total_hours}")


def sum_hours_from_glo_files(directory):
    """
    Scours all subdirectories within a directory for *.glo files and sums the total hours.

    Args:
        directory: The directory to search for subdirectories and *.glo files.

    Returns:
        The total sum of hours extracted from all *.glo files found.
    """

    total_hours = 0
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".glo"):
                filepath = os.path.join(root, filename)
                total_hours += get_hours_from_file(filepath)

    return total_hours


if __name__ == "__main__":
    main()
