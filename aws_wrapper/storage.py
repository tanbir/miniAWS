import boto3
from aws_wrapper.aws_manager import AWSManager

class Storage(AWSManager):
    def __init__(self, region="us-east-1"):
        super().__init__(region)
        self.s3 = boto3.client("s3", region_name=self.region)

    def create_bucket(self, bucket_name):
        self.s3.create_bucket(Bucket=bucket_name)
        return f"Bucket '{bucket_name}' created successfully."

    def upload_file(self, bucket_name, key, content):
        self.s3.put_object(Bucket=bucket_name, Key=key, Body=content)
        return f"File '{key}' uploaded to bucket '{bucket_name}'."

    def list_buckets(self):
        return self.s3.list_buckets()["Buckets"]

    def list_objects(self, bucket_name):
        return self.s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])

    def delete_object(self, bucket_name, key):
        self.s3.delete_object(Bucket=bucket_name, Key=key)
        return f"Object '{key}' deleted from bucket '{bucket_name}'."
