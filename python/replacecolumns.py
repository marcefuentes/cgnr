import os
import pandas as pd

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            df = pd.read_csv(file_path)
            for col in df.columns:
                if col.startswith('w'):
                    df[col] = (df[col] / 2.0).round(6)
            df.to_csv(file_path, index=False)
