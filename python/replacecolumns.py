import os
import pandas as pd

# Step 1: Traverse through the directory
for root, dirs, files in os.walk('.'):
    for file in files:
        # Step 2: Check if the file is a CSV file
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            # Step 3: Load the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            # Step 4: Iterate over the columns in the DataFrame
            for col in df.columns:
                # Step 5: Check if the column name starts with 'w'
                if col.startswith('w'):
                    # Step 6: Divide the column by 2 and round to 6 decimal places
                    df[col] = (df[col] / 2.0).round(6)
            # Step 7: Save the DataFrame back to the CSV file
            df.to_csv(file_path, index=False)
