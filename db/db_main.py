# import libraries
import os
import sys

# import functions from modules
from create_table import create_dynamodb_table
from csv_to_db import upload_csv_to_dynamodb
from query_test import show_custom_lines_from_dynamodb

# Run the script from the command line
if __name__ == "__main__":
    print("")
    if len(sys.argv) != 4: # accept only three arguments
        print("Usage: python db_main.py <formatted_csv_file_name> <table_name> <query_limit>")
        sys.exit(1)

    csv_file_path = "../spreadsheets/" + sys.argv[1]
    table_name = sys.argv[2]
    query_limit = int(sys.argv[3])

    if not os.path.isfile(csv_file_path): # check if the file exists
        print(f"Error: File {csv_file_path} does not exist.")
        sys.exit(1) # exit if the file does not exist

    print(f"Creating table {table_name}...")
    create_dynamodb_table(table_name)
    print("")

    print(f"Uploading {csv_file_path} to {table_name}...")
    upload_csv_to_dynamodb(csv_file_path, table_name)
    print("")

    print(f"Showing {query_limit} lines from {table_name}...")
    show_custom_lines_from_dynamodb(table_name, limit=query_limit)
