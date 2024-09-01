'''This script creates a table in DyanmoDB.'''

# import libraries
import boto3


def create_dynamodb_table(table_name):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000") # note that it is not 'https' but 'http'

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

# Example usage
# table_name = 'BBC-local-table'
# create_dynamodb_table(table_name)
