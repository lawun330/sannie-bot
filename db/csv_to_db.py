import boto3
import pandas as pd

def upload_csv_to_dynamodb(csv_file_path, table_name):
    # read csv
    df = pd.read_csv(csv_file_path)

    # establish DynamoDB connection
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table(table_name)

    # put csv into table
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = row.to_dict() # convert row to dict
            item['uuid'] = str(item['uuid']) # change uuid to string
            batch.put_item(Item=item) # put item to db

    print(f'The file "{csv_file_path}" is exported to the DynamoDB table "{table_name}" successfully.')

# Example usage
# csv_file_path = './spreadsheets/BBC_webscraped_from_python_formatted.csv'
# table_name = 'BBC-local-table'
# upload_csv_to_dynamodb(csv_file_path, table_name)