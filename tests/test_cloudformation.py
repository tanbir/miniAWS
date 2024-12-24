import unittest
from moto import mock_aws
import boto3
from aws_wrapper.cloudformation import CloudFormation


class TestCloudFormation(unittest.TestCase):
    def setUp(self):
        self.cloudformation = CloudFormation(region="us-east-1")

    @mock_aws
    def test_create_and_delete_stack(self):
        self.cloudformation.cloudformation = boto3.client("cloudformation", region_name="us-east-1")

        # Sample template
        template_body = """{
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": "my-test-bucket"
                    }
                }
            }
        }"""

        # Test stack creation
        response = self.cloudformation.create_stack("TestStack", template_body)
        self.assertEqual(response, "CloudFormation stack 'TestStack' creation initiated.")

        # Test listing stacks
        stacks = self.cloudformation.list_stacks()
        self.assertIn("TestStack", stacks)

        # Test stack deletion
        response = self.cloudformation.delete_stack("TestStack")
        self.assertEqual(response, "CloudFormation stack 'TestStack' deletion initiated.")

        # Test listing stacks after deletion
        stacks = self.cloudformation.list_stacks()
        self.assertNotIn("TestStack", stacks)

    @mock_aws
    def test_validate_template(self):
        self.cloudformation.cloudformation = boto3.client("cloudformation", region_name="us-east-1")

        # Valid template
        template_body = """{
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": "my-valid-bucket"
                    }
                }
            }
        }"""

        response = self.cloudformation.validate_template(template_body)
        self.assertIn("Description", response)

    @mock_aws
    def test_describe_stack(self):
        self.cloudformation.cloudformation = boto3.client("cloudformation", region_name="us-east-1")

        # Sample template
        template_body = """{
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": "my-test-bucket"
                    }
                }
            }
        }"""

        # Create stack
        self.cloudformation.create_stack("TestStack", template_body)

        # Test describing stack
        stack = self.cloudformation.describe_stack("TestStack")
        self.assertEqual(stack["StackName"], "TestStack")

    @mock_aws
    def test_describe_stack_resources(self):
        self.cloudformation.cloudformation = boto3.client("cloudformation", region_name="us-east-1")

        # Sample template
        template_body = """{
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": "my-test-bucket"
                    }
                }
            }
        }"""

        # Create stack
        self.cloudformation.create_stack("TestStack", template_body)

        # Test describing stack resources
        resources = self.cloudformation.describe_stack_resources("TestStack")
        self.assertEqual(resources[0]["LogicalResourceId"], "MyBucket")


    @mock_aws
    def test_stack_policy_operations(self):
        self.cloudformation.cloudformation = boto3.client("cloudformation", region_name="us-east-1")

        # Sample template
        template_body = """{
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": "my-policy-test-bucket"
                    }
                }
            }
        }"""

        # Create stack
        self.cloudformation.create_stack("TestStack", template_body)

        # Set stack policy
        stack_policy = """{
            "Statement": [
                {
                    "Effect": "Deny",
                    "Action": "Update:*",
                    "Principal": "*",
                    "Resource": "*"
                }
            ]
        }"""
        response = self.cloudformation.set_stack_policy("TestStack", stack_policy)
        self.assertEqual(response, "Stack policy set for stack 'TestStack'.")

        # Get stack policy
        policy = self.cloudformation.get_stack_policy("TestStack")
        self.assertIn("Deny", policy)


if __name__ == "__main__":
    unittest.main()
