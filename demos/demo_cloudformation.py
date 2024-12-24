import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moto import mock_aws
from aws_wrapper.cloudformation import CloudFormation

@mock_aws
def main():
    # Initialize CloudFormation wrapper
    cloudformation = CloudFormation(region="us-east-1")

    # Template for stack creation
    template_body = """{
        "Resources": {
            "MyBucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "demo-cloudformation-bucket"
                }
            }
        }
    }"""

    print("\n--- Stack Creation ---")
    stack_name = "DemoStack"
    print(cloudformation.create_stack(stack_name, template_body))

    print("\n--- List Stacks ---")
    stacks = cloudformation.list_stacks()
    print("Stacks:", stacks)

    print("\n--- Describe Stack ---")
    stack_description = cloudformation.describe_stack(stack_name)
    print("Description:", stack_description)

    print("\n--- Update Stack ---")
    updated_template_body = """{
        "Resources": {
            "MyBucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "updated-cloudformation-bucket"
                }
            }
        }
    }"""
    print(cloudformation.update_stack(stack_name, updated_template_body))

    print("\n--- List Stacks After Update ---")
    stacks_after_update = cloudformation.list_stacks()
    print("Stacks:", stacks_after_update)

    print("\n--- Delete Stack ---")
    print(cloudformation.delete_stack(stack_name))

    print("\n--- List Stacks After Deletion ---")
    stacks_after_deletion = cloudformation.list_stacks()
    print("Stacks:", stacks_after_deletion)


if __name__ == "__main__":
    main()
