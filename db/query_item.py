'''This script queries an item from the DynamoDB table.'''

# import libraries
import boto3


def show_custom_lines_from_dynamodb(table_name, limit):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table(table_name)

    try:
        response = table.scan(Limit=limit) # limit the number of items to be returned
        items = response.get('Items', [])
        for item in items:
            print(item)
            print("")
    except Exception as e:
        print(f"Error scanning table: {e}")

# Example usage
# table_name = 'BBC-local-table'
# limit = 2
# show_custom_lines_from_dynamodb(table_name, limit)
