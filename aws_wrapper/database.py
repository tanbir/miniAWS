import boto3
from aws_wrapper.aws_manager import AWSManager


class Database(AWSManager):
    def __init__(self, region="us-east-1"):
        super().__init__(region)
        self.dynamodb = boto3.client("dynamodb", region_name=self.region)

    def create_table(self, table_name, key_schema, attribute_definitions, provisioned_throughput):
        """
        Creates a DynamoDB table.

        :param table_name: Name of the table.
        :param key_schema: Key schema for the table.
        :param attribute_definitions: Attribute definitions for the table.
        :param provisioned_throughput: Provisioned throughput configuration.
        :return: Success message.
        """
        self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provisioned_throughput,
        )
        return f"Table '{table_name}' created successfully."

    def describe_table(self, table_name):
        """
        Retrieves metadata about a DynamoDB table.

        :param table_name: Name of the table.
        :return: Metadata of the table as a dictionary.
        """
        response = self.dynamodb.describe_table(TableName=table_name)
        return response["Table"]

    def put_item(self, table_name, item):
        """
        Adds an item to a DynamoDB table.

        :param table_name: Name of the table.
        :param item: Item to add.
        :return: Success message.
        """
        self.dynamodb.put_item(TableName=table_name, Item=item)
        return f"Item added to table '{table_name}'."

    def scan_table(self, table_name):
        """
        Retrieves all items from a DynamoDB table.

        :param table_name: Name of the table.
        :return: List of items.
        """
        response = self.dynamodb.scan(TableName=table_name)
        return response.get("Items", [])

    def query_items(self, table_name, key_condition_expression, expression_attribute_values):
        """
        Queries items in a DynamoDB table using a key condition expression.

        :param table_name: Name of the table.
        :param key_condition_expression: Key condition expression to match.
        :param expression_attribute_values: Dictionary of attribute values for the condition.
        :return: List of matching items.
        """
        response = self.dynamodb.query(
            TableName=table_name,
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
        return response.get("Items", [])

    def update_item(self, table_name, key, update_expression, expression_attribute_values, expression_attribute_names=None):
        """
        Updates an item in a DynamoDB table.

        :param table_name: Name of the table.
        :param key: Primary key of the item to update.
        :param update_expression: Expression specifying attributes to update.
        :param expression_attribute_values: Dictionary of values used in the update expression.
        :param expression_attribute_names: Optional dictionary of attribute name aliases for reserved keywords.
        :return: Success message.
        """
        update_params = {
            "TableName": table_name,
            "Key": key,
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": expression_attribute_values,
        }
        if expression_attribute_names:
            update_params["ExpressionAttributeNames"] = expression_attribute_names

        self.dynamodb.update_item(**update_params)
        return f"Item updated in table '{table_name}'."

    def delete_item(self, table_name, key):
        """
        Deletes an item from a DynamoDB table.

        :param table_name: Name of the table.
        :param key: Primary key of the item to delete.
        :return: Success message.
        """
        self.dynamodb.delete_item(TableName=table_name, Key=key)
        return f"Item deleted from table '{table_name}'."

    def delete_table(self, table_name):
        """
        Deletes a DynamoDB table.

        :param table_name: Name of the table to delete.
        :return: Success message.
        """
        self.dynamodb.delete_table(TableName=table_name)
        return f"Table '{table_name}' deleted successfully."

    def batch_write_items(self, table_name, items):
        """
        Inserts multiple items into a DynamoDB table using a batch write operation.

        :param table_name: Name of the table.
        :param items: List of items to insert.
        :return: Success message.
        """
        with self.dynamodb.batch_writer(TableName=table_name) as batch:
            for item in items:
                batch.put_item(Item=item)
        return f"Batch write to table '{table_name}' completed successfully."
