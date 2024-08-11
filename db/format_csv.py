'''
This script formats a csv file by adding a new column to the left with a unique id created from hashing the dataframe
'''

import pandas as pd
import os
import sys

def format_csv(file): # change the file name to the file you want to format

    # Define a new file name and path
    file_name = os.path.basename(file)
    file_name_without_extension = file_name.split('.')[0]
    file_path = os.path.join('../spreadsheets/', file_name_without_extension + '_formatted.csv')

    # Read the csv file
    df = pd.read_csv(file)

    # Adding a new column to the left with a unique id created from hashing the dataframe
    df.insert(0, 'uuid', pd.util.hash_pandas_object(df).astype(str))
    
    # Make a new csv file
    df.to_csv(file_path, index=False)
    print(f'File {file} formatted and saved as {file_path}')

# Run the script from the command line
if __name__ == "__main__":
    if len(sys.argv) != 2: # accept only one argument
        print("Usage: python format_csv.py <path_of_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]

    if not os.path.isfile(csv_file_path): # check if the file exists
        print(f"Error: File {csv_file_path} does not exist.")
        sys.exit(1) # exit if the file does not exist

    format_csv(csv_file_path)
