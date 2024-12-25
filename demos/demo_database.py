import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_wrapper.database import Database
from moto import mock_aws
import boto3


@mock_aws
def main():
    # Initialize Database wrapper
    database = Database(region="us-east-1")

    print("\n--- Table Management ---")
    # Create a DynamoDB table
    table_name = "DemoTable"
    key_schema = [{"AttributeName": "id", "KeyType": "HASH"}]
    attribute_definitions = [{"AttributeName": "id", "AttributeType": "S"}]
    provisioned_throughput = {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    print(database.create_table(table_name, key_schema, attribute_definitions, provisioned_throughput))

    # Describe the table
    table_info = database.describe_table(table_name)
    print(f"Table Info: {table_info}")

    print("\n--- Item Operations ---")
    # Add an item to the table
    item = {"id": {"S": "1"}, "name": {"S": "Alice"}, "age": {"N": "30"}}
    print(database.put_item(table_name, item))

    # Scan the table
    items = database.scan_table(table_name)
    print(f"Items in table: {items}")

    # Query an item (using an exact match)
    key_condition_expression = "id = :id"
    expression_attribute_values = {":id": {"S": "1"}}
    queried_items = database.query_items(table_name, key_condition_expression, expression_attribute_values)
    print(f"Queried Items: {queried_items}")

    # Update an item
    update_expression = "SET #name = :name, age = :age"
    expression_attribute_values = {":name": {"S": "Alice Updated"}, ":age": {"N": "31"}}
    expression_attribute_names = {"#name": "name"}
    print(database.update_item(table_name, {"id": {"S": "1"}}, update_expression, expression_attribute_values, expression_attribute_names))

    # Scan again to see updated items
    updated_items = database.scan_table(table_name)
    print(f"Updated Items: {updated_items}")

    # Delete an item
    print(database.delete_item(table_name, {"id": {"S": "1"}}))

    print("\n--- Batch Operations ---")
    # Batch write multiple items
    batch_items = [
        {"id": {"S": "2"}, "name": {"S": "Bob"}, "age": {"N": "25"}},
        {"id": {"S": "3"}, "name": {"S": "Charlie"}, "age": {"N": "28"}},
    ]

    print("\n--- Table Deletion ---")
    # Delete the table
    print(database.delete_table(table_name))

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
