import unittest
from moto import mock_aws  # Unified decorator for mocking AWS services
import boto3
from aws_wrapper.storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()

    @mock_aws
    def test_create_and_list_buckets(self):
        # Reinitialize boto3 client within the mock context
        self.storage.s3 = boto3.client("s3", region_name="us-east-1")

        bucket_name = "test-bucket"
        self.assertEqual(
            self.storage.create_bucket(bucket_name),
            f"Bucket '{bucket_name}' created successfully.",
        )
        buckets = self.storage.list_buckets()
        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0]["Name"], bucket_name)

    @mock_aws
    def test_upload_and_list_objects(self):
        # Reinitialize boto3 client within the mock context
        self.storage.s3 = boto3.client("s3", region_name="us-east-1")

        bucket_name = "test-bucket"
        self.storage.create_bucket(bucket_name)
        self.storage.upload_file(bucket_name, "test.txt", "This is a test file.")
        objects = self.storage.list_objects(bucket_name)
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0]["Key"], "test.txt")

    @mock_aws
    def test_download_object(self):
        # Reinitialize boto3 client within the mock context
        self.storage.s3 = boto3.client("s3", region_name="us-east-1")

        bucket_name = "test-bucket"
        file_key = "test.txt"
        file_content = "This is a test file."

        # Upload a file
        self.storage.create_bucket(bucket_name)
        self.storage.upload_file(bucket_name, file_key, file_content)

        # Download the file
        downloaded_content = self.storage.s3.get_object(Bucket=bucket_name, Key=file_key)["Body"].read().decode()
        self.assertEqual(downloaded_content, file_content)

    @mock_aws
    def test_delete_object_and_bucket(self):
        # Reinitialize boto3 client within the mock context
        self.storage.s3 = boto3.client("s3", region_name="us-east-1")

        bucket_name = "test-bucket"
        file_key = "test.txt"

        # Upload a file
        self.storage.create_bucket(bucket_name)
        self.storage.upload_file(bucket_name, file_key, "This is a test file.")

        # Delete the object
        self.assertEqual(
            self.storage.delete_object(bucket_name, file_key),
            f"Object '{file_key}' deleted from bucket '{bucket_name}'."
        )

        # Verify object deletion
        objects = self.storage.list_objects(bucket_name)
        self.assertEqual(len(objects), 0)

        # Delete the bucket
        self.storage.s3.delete_bucket(Bucket=bucket_name)

        # Verify bucket deletion
        buckets = self.storage.list_buckets()
        self.assertEqual(len(buckets), 0)
