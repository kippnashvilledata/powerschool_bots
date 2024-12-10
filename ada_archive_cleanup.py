import os
import pandas as pd
import re

# Directory containing the CSV files
directory = '/home/KIPPNashvilleData/ps_downloads'

# Old column name to be changed
old_column_name = 'grade(track)'

# New column name
new_column_name = 'grade'

# Regular expression pattern to match the file naming convention
pattern = r'^ada_adm_(19|20)\d{2}\.csv$'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if the file name matches the pattern
    if re.match(pattern, filename):
        file_path = os.path.join(directory, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Rename the column
        if old_column_name in df.columns:
            df.rename(columns={old_column_name: new_column_name}, inplace=True)
        
        # Save the DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

print("Column names updated successfully in the matching CSV files.")
