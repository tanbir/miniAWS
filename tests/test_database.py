import unittest
from moto import mock_aws  # Unified decorator for all AWS services
import boto3
from aws_wrapper.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database()
    
    @mock_aws
    def test_create_and_describe_table(self):
        table_name = "test-table"
        self.database.dynamodb = boto3.client("dynamodb", region_name="us-east-1")

        self.database.create_table(
            table_name,
            key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
            attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
            provisioned_throughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        table_metadata = self.database.describe_table(table_name)
        self.assertEqual(table_metadata["TableName"], table_name)

    @mock_aws
    def test_put_and_scan_items(self):
        table_name = "test-table"
        self.database.dynamodb = boto3.client("dynamodb", region_name="us-east-1")

        self.database.create_table(
            table_name,
            key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
            attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
            provisioned_throughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        self.database.put_item(table_name, {"id": {"S": "1"}, "name": {"S": "Alice"}})
        items = self.database.scan_table(table_name)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["name"]["S"], "Alice")

    @mock_aws
    def test_update_and_delete_item(self):
        table_name = "test-table"
        self.database.dynamodb = boto3.client("dynamodb", region_name="us-east-1")

        self.database.create_table(
            table_name,
            key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
            attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
            provisioned_throughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        self.database.put_item(table_name, {"id": {"S": "1"}, "name": {"S": "Alice"}})

        self.database.update_item(
            table_name,
            key={"id": {"S": "1"}},
            update_expression="SET #name = :name",
            expression_attribute_values={":name": {"S": "Updated Alice"}},
            expression_attribute_names={"#name": "name"},
        )
        updated_items = self.database.scan_table(table_name)
        self.assertEqual(updated_items[0]["name"]["S"], "Updated Alice")

        self.database.delete_item(table_name, {"id": {"S": "1"}})
        items_after_deletion = self.database.scan_table(table_name)
        self.assertEqual(len(items_after_deletion), 0)

    @mock_aws
    def test_delete_table(self):
        table_name = "test-table"
        self.database.dynamodb = boto3.client("dynamodb", region_name="us-east-1")

        self.database.create_table(
            table_name,
            key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
            attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
            provisioned_throughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        self.database.delete_table(table_name)
        with self.assertRaises(Exception):
            self.database.describe_table(table_name)


if __name__ == "__main__":
    unittest.main()
