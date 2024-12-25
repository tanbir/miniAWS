import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_wrapper.storage import Storage
from moto import mock_aws


@mock_aws
def main():
    # Initialize Storage wrapper
    storage = Storage(region="us-east-1")

    print("\n--- Bucket Management ---")
    # Create a bucket
    bucket_name = "demo-bucket"
    print(storage.create_bucket(bucket_name))

    # List all buckets
    buckets = storage.list_buckets()
    print(f"Buckets: {[bucket['Name'] for bucket in buckets]}")

    print("\n--- File Upload ---")
    # Upload a file to the bucket
    file_key = "example.txt"
    file_content = "This is a test file for the demo."
    print(storage.upload_file(bucket_name, file_key, file_content))

    print("\n--- List Objects in Bucket ---")
    # List objects in the bucket
    objects = storage.list_objects(bucket_name)
    print(f"Objects in bucket '{bucket_name}': {[obj['Key'] for obj in objects]}")

    print("\n--- Delete Object ---")
    # Delete an object from the bucket
    print(storage.delete_object(bucket_name, file_key))

    print("\n--- Verify Deletion ---")
    # Verify that the object is deleted
    objects_after_deletion = storage.list_objects(bucket_name)
    print(f"Objects in bucket after deletion: {[obj['Key'] for obj in objects_after_deletion]}")

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
