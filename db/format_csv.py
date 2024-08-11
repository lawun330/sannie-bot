'''
This script formats a csv file by adding a new column to the left with a unique id created from hashing the dataframe
'''

import pandas as pd
import os

def format_csv(file):
    # Define a new file name and path
    file_name = os.path.basename(file)
    file_name_without_extension = file_name.split('.')[0]
    file_path = os.path.join('../spreadsheets/', file_name_without_extension + '_formatted.csv')

    df = pd.read_csv(file)

    # Adding a new column to the left with a unique id created from hashing the dataframe
    df.insert(0, 'uuid', pd.util.hash_pandas_object(df).astype(str))
    
    # Make a new csv file
    df.to_csv(file_path, index=False)

    print(f'File {file} formatted and saved as {file_path}')

# Change the file name to the file you want to format
# Example- format_csv('./spreadsheets/BBC_webscraped.csv')
format_csv('../spreadsheets/BBC_webscraped.csv')