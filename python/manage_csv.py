
#!/usr/bin/env python3

import sys

from tools.csv_tools import call_function

def main():
    """Manages CSV operations by calling functions from csv_tools.py"""

    # Check for required arguments (function name and potentially arguments)
    if len(sys.argv) < 2:
        print("Error: Please provide a function name and any required arguments.")
        print("Usage: manage_csv.py <function_name> [arguments]")
        sys.exit(1)

    # Get function name and separate arguments (if any)
    function_name = sys.argv[1]
    args = sys.argv[2:]

    try:
        call_function(function_name, *args)
    except AttributeError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
  main()

